local process = require("practice.process")
local log = require("practice.log")
local ui = require("problem_solving.ui")
local sync = require("problem_solving.sync")
local statusline = require("problem_solving.statusline")

local M = {}
local config, stats_pending = nil, false
local rating_values = {
  again = "fail", hard = "acceptable", good = "good", easy = "excellent",
  fail = "fail", acceptable = "acceptable", excellent = "excellent",
}
local rating_labels = { fail = "Again", acceptable = "Hard", good = "Good", excellent = "Easy" }

local state = {
  status = "idle",
  collection = nil,
  previous_id = nil,
  problem = nil,
  next_due = nil,
  open_bookmarks = 0,
  bookmarked = false,
  conversation_history = {},
  conversation_pending = false,
  conversation_notice = nil,
  hint_requested = false,
  outline_revealed = false,
  operation = 0,
  timing = { phase = nil, started = nil, focused = true, solve_ms = 0, discussion_ms = 0 },
}

local function script(name) return config.scripts_dir .. "/" .. name end

local function flush_timing()
  if not state.timing.phase or not state.timing.started then return end
  local elapsed = math.floor((vim.uv.hrtime() - state.timing.started) / 1000000)
  local field = state.timing.phase .. "_ms"
  state.timing[field] = state.timing[field] + math.max(0, elapsed)
  state.timing.started = nil
end

local function timing_phase(phase)
  flush_timing()
  state.timing.phase = phase
  if phase and state.timing.focused then state.timing.started = vim.uv.hrtime() end
end

local function reset_timing()
  state.timing.phase, state.timing.started = nil, nil
  state.timing.solve_ms, state.timing.discussion_ms = 0, 0
end

local function request(name, body, callback)
  state.operation = state.operation + 1
  local operation = state.operation
  return process.run(config.python, script(name), body, function(error_message, response)
    if operation ~= state.operation then return end
    callback(error_message, response)
  end)
end

local function base_request()
  return { collection_directory = state.collection, database_path = config.database_path }
end

local function valid_state(value)
  return type(value) == "table"
    and type(value.hint_requested) == "boolean"
    and type(value.revealed) == "boolean"
end

local function show_problem(problem, response, bookmarked)
  if type(problem) ~= "table" or type(problem.id) ~= "string"
    or type(problem.brief_path) ~= "string" or not valid_state(response.state)
  then
    state.status = "idle"
    ui.notify("Problem selection returned an invalid response", vim.log.levels.ERROR)
    return
  end
  state.problem = problem
  state.previous_id = problem.id
  state.bookmarked = bookmarked == true
  state.conversation_history = config.retain_conversation_history
    and type(response.state.conversation_history) == "table"
    and response.state.conversation_history or {}
  state.conversation_pending = false
  state.conversation_notice = nil
  state.hint_requested = response.state.hint_requested
  state.outline_revealed = response.state.revealed
  reset_timing()
  ui.open_brief(problem, response.hint)
  if response.state.revealed then
    state.status = "revealed"
    ui.open_outline(response)
    timing_phase("discussion")
  else
    state.status = "solving"
    timing_phase("solve")
  end
  log.event("problem_opened", "info", {
    problem_id = problem.id,
    bookmarked = state.bookmarked,
    hint_requested = response.state.hint_requested,
    revealed = response.state.revealed,
  })
end

local function select_next()
  state.operation = state.operation + 1
  ui.close_all()
  state.problem, state.bookmarked, state.next_due = nil, false, nil
  state.conversation_history, state.conversation_pending = {}, false
  state.conversation_notice = nil
  state.hint_requested, state.outline_revealed = false, false
  reset_timing()
  state.status = "selecting"
  local body = base_request()
  body.previous_problem_id = state.previous_id
  request("select_problem_solving_card.py", body, function(error_message, response)
    if error_message then
      state.status = "idle"
      ui.notify("Selection failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    state.open_bookmarks = response.open_bookmarks or 0
    if response.problem == nil or response.problem == vim.NIL then
      state.status = "complete"
      state.next_due = response.next_due ~= vim.NIL and response.next_due or nil
      local message = state.next_due and "No problems are due. Next review: " .. state.next_due
        or "No unbookmarked problems are currently available."
      ui.notify(message)
      return
    end
    local problem = response.problem
    request("problem_solving_card.py", vim.tbl_extend("force", base_request(), {
      problem_id = problem.id, action = "get",
    }), function(card_error, card_response)
      if card_error then
        state.status = "idle"
        ui.notify("Could not restore problem state: " .. card_error, vim.log.levels.ERROR)
        return
      end
      show_problem(problem, card_response, false)
    end)
  end)
end

local function refresh_card(action, extra, callback, on_error)
  if not state.problem then return end
  local body = vim.tbl_extend("force", base_request(), {
    problem_id = state.problem.id,
    action = action,
  }, extra or {})
  request("problem_solving_card.py", body, function(error_message, response)
    if error_message then
      ui.notify("Problem action failed: " .. error_message, vim.log.levels.ERROR)
      if on_error then on_error() end
      return
    end
    if not valid_state(response.state) then
      ui.notify("Problem action returned invalid state", vim.log.levels.ERROR)
      return
    end
    if callback then callback(response) end
  end)
end

function M.setup(options) config = options end

function M.focus_lost()
  flush_timing()
  state.timing.focused = false
end

function M.focus_gained()
  state.timing.focused = true
  if state.timing.phase and not state.timing.started then state.timing.started = vim.uv.hrtime() end
end

function M.start(directory)
  if state.status == "selecting" or state.status == "recording" then
    ui.notify("Wait for the current problem-solving operation", vim.log.levels.WARN)
    return
  end
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  state.operation = state.operation + 1
  state.collection = directory and vim.fn.fnamemodify(directory, ":p") or config.default_directory
  state.previous_id = nil
  sync.trigger(state.collection)
  select_next()
end

function M.hint()
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if state.status ~= "solving" then
    ui.notify("A hint is available only before reveal", vim.log.levels.WARN)
    return
  end
  refresh_card("hint", nil, function(response)
    state.hint_requested = response.state.hint_requested
    ui.open_brief(state.problem, response.hint)
    ui.notify("Optional hint revealed")
  end)
end

function M.reveal()
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if state.status ~= "solving" then
    ui.notify("Reveal is available only while solving", vim.log.levels.WARN)
    return
  end
  timing_phase(nil)
  refresh_card("reveal", nil, function(response)
    state.status = "revealed"
    state.outline_revealed = true
    ui.open_brief(state.problem, response.hint)
    ui.open_outline(response)
    timing_phase("discussion")
    ui.notify("Solution outline revealed")
    if state.bookmarked then
      ui.notify("This problem is bookmarked; retain it for more thought or use "
        .. ":ProblemSolvingUnbookmark before rating.")
    end
  end, function() timing_phase("solve") end)
end

function M.bookmark(note)
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if state.status ~= "solving" and state.status ~= "revealed" and state.status ~= "discussing" then
    ui.notify("Bookmark is available only for an active problem", vim.log.levels.WARN)
    return
  end
  local body = vim.tbl_extend("force", base_request(), {
    action = state.bookmarked and "update" or "create",
    problem_id = state.problem.id,
  })
  if note ~= nil then body.note = note end
  local was_bookmarked = state.bookmarked
  local previous_status = state.status
  state.status = "bookmarked"
  timing_phase(nil)
  request("problem_solving_bookmark.py", body, function(error_message)
    if error_message then
      state.status = previous_status
      timing_phase(previous_status ~= "solving" and "discussion" or "solve")
      ui.notify("Bookmark failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    state.bookmarked = true
    ui.notify(was_bookmarked and "Bookmark updated" or "Problem added to open-thinking queue")
    if was_bookmarked then
      state.status = previous_status
      refresh_card("get", nil, function(response)
        state.status = response.state.revealed and "revealed" or "solving"
        state.hint_requested = response.state.hint_requested
        state.outline_revealed = response.state.revealed
        timing_phase(response.state.revealed and "discussion" or "solve")
      end)
    else
      select_next()
    end
  end)
end

function M.note(note)
  if note == nil then
    vim.ui.input({ prompt = "Private bookmark note: " }, function(value)
      if value ~= nil then M.note(value) end
    end)
    return
  end
  M.bookmark(tostring(note))
end

function M.bookmarks()
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if not state.collection then
    ui.notify("Start problem-solving practice first", vim.log.levels.WARN)
    return
  end
  request("problem_solving_bookmark.py",
    vim.tbl_extend("force", base_request(), { action = "list" }),
    function(error_message, response)
      if error_message or type(response.bookmarks) ~= "table" then
        ui.notify("Could not load bookmarks: " .. tostring(error_message), vim.log.levels.ERROR)
        return
      end
      ui.open_bookmarks(response.bookmarks, M.reopen)
    end)
end

function M.reopen(problem_id)
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if not state.collection or type(problem_id) ~= "string" or problem_id == "" then return end
  state.operation = state.operation + 1
  request("problem_solving_card.py", vim.tbl_extend("force", base_request(), {
    problem_id = problem_id, action = "get",
  }), function(error_message, response)
    if error_message then
      ui.notify("Could not reopen bookmark: " .. error_message, vim.log.levels.ERROR)
      return
    end
    local first = vim.fn.readfile(response.brief_path, "", 1)[1] or problem_id
    show_problem({ id = problem_id, title = first:gsub("^#%s*", ""), brief_path = response.brief_path },
      response, true)
  end)
end

function M.unbookmark()
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if not state.problem or not state.bookmarked then
    ui.notify("The active problem is not bookmarked", vim.log.levels.WARN)
    return
  end
  request("problem_solving_bookmark.py", vim.tbl_extend("force", base_request(), {
    action = "remove", problem_id = state.problem.id,
  }), function(error_message)
    if error_message then
      ui.notify("Could not remove bookmark: " .. error_message, vim.log.levels.ERROR)
      return
    end
    state.bookmarked = false
    ui.notify("Problem removed from open-thinking queue")
  end)
end

function M.rate(rating)
  local internal = rating_values[(rating or ""):lower()]
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if state.status ~= "revealed" and state.status ~= "discussing" then
    ui.notify("Rate only after revealing the solution outline", vim.log.levels.WARN)
    return
  end
  if not internal then
    ui.notify("Rating must be Again, Hard, Good, or Easy", vim.log.levels.ERROR)
    return
  end
  timing_phase(nil)
  state.status = "recording"
  request("record_problem_solving_rating.py", vim.tbl_extend("force", base_request(), {
    problem_id = state.problem.id,
    final_rating = internal,
    solve_duration_ms = state.timing.solve_ms,
    discussion_duration_ms = state.timing.discussion_ms,
  }), function(error_message, response)
    if error_message or response.recorded ~= true then
      state.status = "revealed"
      timing_phase("discussion")
      ui.notify("Rating failed: " .. tostring(error_message), vim.log.levels.ERROR)
      return
    end
    ui.notify("Rated " .. rating_labels[internal])
    sync.trigger(state.collection)
    statusline.invalidate(state.collection)
    select_next()
  end)
end

function M.begin_discussion()
  if state.status ~= "revealed" and state.status ~= "discussing" then
    ui.notify("Discussion is available only after reveal", vim.log.levels.WARN)
    return false
  end
  state.status = "discussing"
  return true
end

function M.ask(question)
  if state.status ~= "solving" and state.status ~= "revealed" and state.status ~= "discussing" then
    ui.notify("Conversation is available only while a problem is active", vim.log.levels.WARN)
    return
  end
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if question == nil then
    vim.ui.input({ prompt = state.status == "solving" and "Ask for clarification: "
      or "Discuss solution: " }, function(value)
      if value ~= nil then M.ask(value) end
    end)
    return
  end
  question = vim.trim(tostring(question))
  if question == "" then return end

  local was_solving = state.status == "solving"
  local resume_status = was_solving and "solving" or "discussing"
  local reviewer = was_solving and config.clarification_reviewer or config.discussion_reviewer
  state.status = resume_status
  state.conversation_pending = true
  state.conversation_notice = nil
  timing_phase(nil)
  ui.open_conversation(state.conversation_history, { question = question }, nil)
  local body = vim.tbl_extend("force", base_request(), {
    problem_id = state.problem.id,
    question = question,
    history = state.conversation_history,
    retain_conversation_history = config.retain_conversation_history,
    reviewer = reviewer,
  })
  request(was_solving and "level_c_clarify.py" or "level_c_discuss.py", body,
    function(error_message, response)
      state.conversation_pending = false
      state.status = resume_status
      timing_phase(was_solving and "solve" or "discussion")
      if error_message then
        state.conversation_notice = "The conversation request failed. Practice remains available."
        ui.open_conversation(state.conversation_history, nil, state.conversation_notice)
        ui.notify("Conversation request failed", vim.log.levels.ERROR)
        return
      end
      if response.status == "unavailable" then
        state.conversation_notice = "The reviewer is unavailable. You can continue practicing."
        ui.open_conversation(state.conversation_history, nil, state.conversation_notice)
        ui.notify("Conversation reviewer unavailable", vim.log.levels.WARN)
        return
      end
      if type(response.answer) ~= "string"
        or type(response.conversation_history) ~= "table"
      then
        state.conversation_notice = "The reviewer returned an invalid response. Practice remains available."
        ui.open_conversation(state.conversation_history, nil, state.conversation_notice)
        ui.notify("Conversation response was invalid", vim.log.levels.ERROR)
        return
      end
      state.conversation_history = response.conversation_history
      ui.open_conversation(state.conversation_history, nil, nil)
      if response.status == "redirected" then
        ui.notify("That question would reveal solving guidance")
      end
    end)
end

function M.next()
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  if state.status ~= "solving" and state.status ~= "revealed" and state.status ~= "discussing" then
    ui.notify("Next is available only while a problem is active", vim.log.levels.WARN)
    return
  end
  select_next()
end

function M.stats(directory)
  if stats_pending then return end
  local collection = directory and vim.fn.fnamemodify(directory, ":p")
    or state.collection or config.default_directory
  stats_pending = true
  process.run(config.python, script("problem_solving_stats.py"), {
    collection_directory = collection, database_path = config.database_path,
  }, function(error_message, response)
    stats_pending = false
    if error_message or type(response.collection_state) ~= "table"
      or type(response.reviews) ~= "table"
    then
      ui.notify("Statistics failed: " .. tostring(error_message), vim.log.levels.ERROR)
      return
    end
    ui.open_stats(response)
  end)
end

function M.quit()
  if state.status == "selecting" or state.status == "recording" then
    ui.notify("Wait for the current problem-solving operation", vim.log.levels.WARN)
    return
  end
  if state.conversation_pending then
    ui.notify("Wait for the current conversation response", vim.log.levels.WARN)
    return
  end
  state.operation = state.operation + 1
  timing_phase(nil)
  ui.close_all()
  state.status, state.collection, state.problem = "idle", nil, nil
  state.previous_id, state.bookmarked, state.next_due = nil, false, nil
  state.conversation_history, state.conversation_pending = {}, false
  state.conversation_notice = nil
  state.hint_requested, state.outline_revealed = false, false
  ui.notify("Problem-solving session ended")
end

function M.get_state() return state end

return M
