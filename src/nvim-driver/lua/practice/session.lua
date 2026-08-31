local process = require("practice.process")
local ui = require("practice.ui")
local import_folds = require("practice.import_folds")
local log = require("practice.log")
local notes = require("practice.notes")
local sync = require("practice.sync")
local statusline = require("practice.statusline")

local M = {}

-- A direct `ZZ` mapping is subject to Neovim's mapping timeout.  Once that
-- timeout expires, the second Z reaches the built-in write-and-quit command.
-- Handle each Z immediately instead, so the practice buffer never exposes the
-- built-in Z commands.
local DOUBLE_Z_GRACE_MS = 5000

local RATINGS = {
  fail = true,
  acceptable = true,
  good = true,
  excellent = true,
}

local state = {
  status = "idle",
  collection = nil,
  collections = nil,
  previous_id = nil,
  exercise = nil,
  result = nil,
  previous_result = nil,
  next_due = nil,
  session_directory = nil,
  working_path = nil,
  source_buffer = nil,
  source_window = nil,
  progress_timer = nil,
  progress_path = nil,
  progress_started = nil,
  progress_events = {},
  progress_event_count = 0,
  follow_up_pending = false,
  compiler_chat_pending = false,
  compiler_result = nil,
  double_z_buffer = nil,
  double_z_timer = nil,
  timing = {
    phase = nil,
    started = nil,
    focused = true,
    solve_ms = 0,
    feedback_ms = 0,
  },
}

local config = nil
local stats_pending = false

local function set_status(status)
  state.status = status
  if config and config.on_status_change then
    config.on_status_change()
  end
end

local function flush_timing()
  if not state.timing.started or not state.timing.phase then return end
  local elapsed_ms = math.floor((vim.uv.hrtime() - state.timing.started) / 1000000)
  local field = state.timing.phase .. "_ms"
  state.timing[field] = state.timing[field] + math.max(0, elapsed_ms)
  state.timing.started = nil
end

local function set_timing_phase(phase)
  flush_timing()
  state.timing.phase = phase
  if phase and state.timing.focused then
    state.timing.started = vim.uv.hrtime()
  end
end

local function reset_timing()
  state.timing.phase = nil
  state.timing.started = nil
  state.timing.solve_ms = 0
  state.timing.feedback_ms = 0
end

local function valid_buffer(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
end

local function valid_window(window)
  return window ~= nil and vim.api.nvim_win_is_valid(window)
end

local function script_path(name)
  return config.scripts_dir .. "/" .. name
end

local function is_modified()
  return valid_buffer(state.source_buffer) and vim.bo[state.source_buffer].modified
end

local function confirm_abandon(action)
  return not is_modified() or ui.confirm_discard(action)
end

local function confirm_exit_while_waiting()
  return vim.fn.confirm(
    "A practice operation is still running. Exit Neovim and stop waiting for it?",
    "&Exit\n&Cancel", 2
  ) == 1
end

local function cancel_double_z()
  local timer = state.double_z_timer
  state.double_z_buffer = nil
  state.double_z_timer = nil
  if timer then
    pcall(function()
      timer:stop()
      timer:close()
    end)
  end
end

local function arm_double_z(buffer)
  cancel_double_z()
  state.double_z_buffer = buffer
  local timer
  timer = vim.defer_fn(function()
    if state.double_z_timer == timer then
      state.double_z_buffer = nil
      state.double_z_timer = nil
    end
  end, DOUBLE_Z_GRACE_MS)
  state.double_z_timer = timer
end

local function install_double_z_mapping(buffer, description)
  vim.keymap.set("n", "Z", function()
    if state.double_z_buffer == buffer then
      cancel_double_z()
      M.zz()
      return
    end
    arm_double_z(buffer)
  end, {
    buffer = buffer,
    silent = true,
    nowait = true,
    desc = description,
  })
end

local function remove_double_z_mapping(buffer)
  if state.double_z_buffer == buffer then
    cancel_double_z()
  end
  if valid_buffer(buffer) then
    pcall(vim.keymap.del, "n", "Z", { buffer = buffer })
  end
end

local function stop_progress()
  if state.progress_timer then
    state.progress_timer:stop()
    state.progress_timer:close()
  end
  state.progress_timer = nil
  state.progress_started = nil
end

local function read_progress()
  if not state.progress_path or vim.fn.filereadable(state.progress_path) ~= 1 then
    return
  end
  local events = {}
  for _, line in ipairs(vim.fn.readfile(state.progress_path)) do
    local ok, event = pcall(vim.json.decode, line)
    if ok and type(event) == "table" then
      table.insert(events, event)
    end
  end
  for index = state.progress_event_count + 1, #events do
    log.event("evaluation_progress", "info", events[index])
  end
  state.progress_event_count = #events
  state.progress_events = events
end

local function start_progress()
  stop_progress()
  state.progress_path = state.session_directory .. "/evaluation-progress.jsonl"
  vim.fn.delete(state.progress_path)
  state.progress_started = vim.uv.hrtime()
  state.progress_events = {}
  state.progress_event_count = 0
  state.follow_up_pending = false
  state.compiler_chat_pending = false
  state.compiler_result = nil
  local progress_buffer = ui.open_progress(state.source_window)
  local timer = vim.uv.new_timer()
  state.progress_timer = timer
  timer:start(0, 100, vim.schedule_wrap(function()
    if state.progress_timer ~= timer then
      return
    end
    read_progress()
    local elapsed = (vim.uv.hrtime() - state.progress_started) / 1000000000
    ui.update_progress(elapsed, state.progress_events)
  end))
  return progress_buffer
end

local function delete_working_copy()
  cancel_double_z()
  reset_timing()
  stop_progress()
  ui.close_feedback()
  if valid_buffer(state.source_buffer) then
    vim.api.nvim_buf_delete(state.source_buffer, { force = true })
  end
  if state.working_path then
    vim.fn.delete(state.working_path)
  end
  state.exercise = nil
  state.result = nil
  state.previous_result = nil
  state.working_path = nil
  state.source_buffer = nil
  state.next_due = nil
  state.progress_path = nil
  state.progress_events = {}
  state.progress_event_count = 0
  state.follow_up_pending = false
end

local function reset_session()
  delete_working_copy()
  if state.session_directory then
    vim.fn.delete(state.session_directory, "rf")
  end
  set_status("idle")
  state.collection = nil
  state.collections = nil
  state.previous_id = nil
  state.session_directory = nil
  state.source_window = nil
end

local function ensure_session_directory()
  if state.session_directory then
    return true
  end
  local path = vim.fn.tempname() .. "-practice"
  if vim.fn.mkdir(path, "p") ~= 1 then
    ui.notify("Could not create practice working directory: " .. path, vim.log.levels.ERROR)
    return false
  end
  state.session_directory = path
  return true
end

local function valid_exercise(exercise)
  return type(exercise) == "table"
    and type(exercise.id) == "string"
    and type(exercise.name) == "string"
    and type(exercise.collection_directory) == "string"
    and type(exercise.source_path) == "string"
    and type(exercise.metadata_path) == "string"
end

local function open_selected_exercise(exercise)
  if not ensure_session_directory() then
    set_status("idle")
    return
  end

  local extension = vim.fn.fnamemodify(exercise.source_path, ":e")
  local working_path = vim.fn.tempname()
  if extension ~= "" then
    working_path = working_path .. "." .. extension
  end
  local copied, copy_error = vim.uv.fs_copyfile(exercise.source_path, working_path)
  if not copied then
    set_status("idle")
    ui.notify("Could not create working copy: " .. tostring(copy_error), vim.log.levels.ERROR)
    return
  end

  state.exercise = exercise
  state.collection = exercise.collection_directory
  state.previous_id = exercise.id
  state.working_path = working_path
  state.source_buffer, state.source_window = ui.open_source(
    working_path,
    state.source_window,
    config.practice_marker,
    config.enhanced_syntax_highlighting,
    config.local_completion
  )
  install_double_z_mapping(state.source_buffer, "Practice: press Z again to submit")
  vim.keymap.set("i", "<C-CR>", function()
    vim.cmd("stopinsert")
    M.submit()
  end, {
    buffer = state.source_buffer,
    silent = true,
    desc = "Practice: submit the current exercise",
  })
  set_status("solving")
  reset_timing()
  set_timing_phase("solve")
end

local function select_next()
  delete_working_copy()
  set_status("selecting")
  process.run(config.python, script_path("select_exercise.py"), {
    exercise_directories = state.collections,
    database_path = config.database_path,
    source_extension = config.source_extension,
    metadata_extension = config.metadata_extension,
    previous_exercise = state.collection and state.previous_id and {
      collection_directory = state.collection,
      exercise_id = state.previous_id,
    } or nil,
  }, function(error_message, response)
    if error_message then
      set_status("idle")
      ui.notify("Selection failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if (response.exercise == nil or response.exercise == vim.NIL) then
      set_status("complete")
      state.next_due = response.next_due
      if type(response.next_due) == "string" then
        ui.notify_next_due(response.next_due)
      else
        ui.notify("No enabled exercises remain in the selected collection")
      end
      return
    end
    if not valid_exercise(response.exercise) then
      set_status("idle")
      ui.notify("Selection failed: invalid exercise response", vim.log.levels.ERROR)
      return
    end
    open_selected_exercise(response.exercise)
  end)
end

function M.setup(options)
  config = options
  notes.setup(options)
  statusline.setup(options, function() return state end)
end

function M.focus_lost()
  state.timing.focused = false
  flush_timing()
end

function M.focus_gained()
  state.timing.focused = true
  if state.timing.phase and not state.timing.started then
    state.timing.started = vim.uv.hrtime()
  end
end

local function note_excerpt(buffer, first_line, last_line)
  local lines = vim.api.nvim_buf_get_lines(buffer, first_line - 1,
    math.min(last_line, first_line + 9), false)
  local excerpt = table.concat(lines, "\n")
  if #excerpt > 1024 then
    excerpt = excerpt:sub(1, 1021) .. "..."
  end
  return excerpt
end

function M.note(kind, first_line, last_line)
  if state.status ~= "solving" and state.status ~= "evaluating"
    and state.status ~= "reviewing" and state.status ~= "post_rating"
  then
    ui.notify("A note can be captured only while an exercise is active", vim.log.levels.WARN)
    return nil
  end
  if not state.exercise then
    ui.notify("The active exercise context is unavailable", vim.log.levels.ERROR)
    return nil
  end

  local buffer = vim.api.nvim_get_current_buf()
  local cursor = vim.api.nvim_win_get_cursor(0)
  local selected = first_line ~= nil
  first_line = first_line or cursor[1]
  last_line = last_line or first_line
  local context_text = nil
  local section = nil
  if buffer == state.source_buffer then
    context_text = state.exercise.source_path .. ":" .. first_line .. ":" .. (cursor[2] + 1)
  else
    local feedback = ui.feedback_context(buffer, first_line)
    if not feedback then
      ui.notify("Open the practice source or feedback buffer before capturing a note",
        vim.log.levels.WARN)
      return nil
    end
    section = feedback.section
    if feedback.metadata_line then
      context_text = state.exercise.metadata_path .. ":" .. feedback.metadata_line
    else
      context_text = state.status == "evaluating" and "evaluation progress" or "practice feedback"
    end
  end

  local composer = notes.compose({
    collection = state.collection,
    exercise_id = state.exercise.id,
    phase = state.status,
    session_id = log.session_id(),
    context = context_text,
    section = section,
    excerpt = note_excerpt(buffer, first_line, selected and last_line or first_line),
    filename_timestamp = os.date("%Y-%m-%d-%H-%M-%S"),
    created_at = os.date("%Y-%m-%d %H:%M:%S %z"),
  }, kind)
  return composer
end

function M.open_notes()
  notes.open_directory()
end

function M.fold_imports()
  if valid_buffer(state.source_buffer) then
    local count = nil
    local opened = nil
    for _, window in ipairs(vim.fn.win_findbuf(state.source_buffer)) do
      if valid_window(window) then
        local window_count, window_opened = import_folds.toggle(state.source_buffer, window)
        count = window_count or count
        opened = window_opened
      end
    end
    if count then
      ui.notify(string.format("%s %d %s", opened and "Opened" or "Folded", count,
        count == 1 and "import" or "imports"),
        vim.log.levels.INFO)
    else
      ui.notify("No import/include preamble found", vim.log.levels.INFO)
    end
  end
end

function M.stats(directory)
  if stats_pending then
    ui.notify("Practice statistics are already loading", vim.log.levels.WARN)
    return
  end
  local collections = directory and { vim.fn.fnamemodify(directory, ":p") }
    or state.collections or config.default_directories
  stats_pending = true
  process.run(config.python, script_path("practice_stats.py"), {
    exercise_directories = collections,
    database_path = config.database_path,
    source_extension = config.source_extension,
    metadata_extension = config.metadata_extension,
    history_days = 30,
  }, function(error_message, response)
    stats_pending = false
    if error_message then
      ui.notify("Statistics failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if type(response.today) ~= "table"
      or type(response.collection_state) ~= "table"
      or type(response.forecast) ~= "table"
      or type(response.history) ~= "table"
      or type(response.collection) ~= "string"
    then
      ui.notify("Statistics failed: invalid response", vim.log.levels.ERROR)
      return
    end
    ui.open_stats(response, function() M.stats(directory) end)
  end)
end

function M.start(directory)
  if state.status == "selecting"
    or state.status == "evaluating"
    or state.status == "recording"
  then
    ui.notify("Wait for the current practice operation to finish", vim.log.levels.WARN)
    return
  end
  if state.follow_up_pending then
    ui.notify("Wait for the current follow-up response", vim.log.levels.WARN)
    return
  end
  if state.status ~= "idle" and not confirm_abandon("restart practice") then
    return
  end
  reset_session()
  state.collections = directory and { vim.fn.fnamemodify(directory, ":p") } or config.default_directories
  state.collection = nil
  statusline.refresh(state.collections)
  sync.trigger(state.collections)
  select_next()
end

local function manage_active_exercise(action)
  if state.status ~= "solving" and state.status ~= "reviewing" and state.status ~= "post_rating" then
    ui.notify("Problem management is available only while an exercise is active", vim.log.levels.WARN)
    return
  end
  if not state.exercise then
    ui.notify("The active exercise context is unavailable", vim.log.levels.ERROR)
    return
  end

  local verb = action == "delete" and "permanently delete" or "disable"
  local detail = action == "delete"
    and "This removes the source, instructions, manifest row, and order entry."
    or "It will no longer be selected. You can re-enable it with :PracticeEnable {id}."
  if vim.fn.confirm(string.format("%s %s?\n%s", verb, state.exercise.name, detail),
      "&Confirm\n&Cancel", 2) ~= 1 then
    return
  end

  local exercise = state.exercise
  process.run(config.python, script_path("manage_exercise.py"), {
    action = action,
    exercise_directory = exercise.collection_directory,
    exercise_id = exercise.id,
    database_path = config.database_path,
    source_extension = config.source_extension,
    metadata_extension = config.metadata_extension,
  }, function(error_message, response)
    if error_message or type(response) ~= "table" or response.managed ~= true then
      ui.notify("Could not " .. verb .. " exercise: " .. tostring(error_message or "invalid response"),
        vim.log.levels.ERROR)
      return
    end
    ui.notify(string.format("%s %s", action == "delete" and "Deleted" or "Disabled", exercise.name))
    statusline.invalidate(state.collections)
    sync.trigger(state.collections)
    select_next()
  end)
end

function M.disable()
  manage_active_exercise("disable")
end

function M.delete()
  manage_active_exercise("delete")
end

function M.enable(directory, exercise_id)
  if type(exercise_id) ~= "string" or exercise_id == "" then
    ui.notify("Provide an exercise ID to re-enable", vim.log.levels.WARN)
    return
  end
  local collection = directory or state.collection
    or (state.collections and #state.collections == 1 and state.collections[1])
  if type(collection) ~= "string" then
    ui.notify("Start a single collection or provide a collection directory", vim.log.levels.WARN)
    return
  end
  process.run(config.python, script_path("manage_exercise.py"), {
    action = "enable",
    exercise_directory = collection,
    exercise_id = exercise_id,
    database_path = config.database_path,
    source_extension = config.source_extension,
    metadata_extension = config.metadata_extension,
  }, function(error_message, response)
    if error_message or type(response) ~= "table" or response.managed ~= true then
      ui.notify("Could not re-enable exercise: " .. tostring(error_message or "invalid response"),
        vim.log.levels.ERROR)
      return
    end
    ui.notify("Enabled " .. exercise_id)
    statusline.invalidate(state.collections or { collection })
    sync.trigger(state.collections or { collection })
  end)
end

function M.submit()
  if state.status ~= "solving" then
    ui.notify("Submit is available only while solving an exercise", vim.log.levels.WARN)
    return
  end
  if not valid_buffer(state.source_buffer) then
    ui.notify("The practice source buffer is no longer available", vim.log.levels.ERROR)
    return
  end

  local saved, save_error = pcall(function()
    vim.api.nvim_buf_call(state.source_buffer, function()
      vim.cmd("silent write")
    end)
  end)
  if not saved then
    ui.notify("Could not save the working copy: " .. tostring(save_error), vim.log.levels.ERROR)
    return
  end

  state.previous_result = nil
  set_timing_phase(nil)
  set_status("evaluating")
  local progress_buffer = start_progress()
  install_double_z_mapping(progress_buffer, "Practice: press Z again to confirm exit")
  process.run(config.python, script_path("evaluate_exercise.py"), {
    source_path = state.working_path,
    starter_source_path = state.exercise.source_path,
    metadata_path = state.exercise.metadata_path,
    target_environment = state.exercise.target_environment,
    command = config.evaluation_command,
    reviewer = config.reviewer,
    progress_path = state.progress_path,
  }, function(error_message, response)
    read_progress()
    stop_progress()
    remove_double_z_mapping(progress_buffer)
    if error_message then
      set_status("solving")
      set_timing_phase("solve")
      ui.show_progress_error(error_message)
      ui.notify("Evaluation failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if type(response.compiled) ~= "boolean"
      or type(response.diagnostics) ~= "string"
      or type(response.metadata) ~= "string"
      or (response.metadata_sections ~= nil and response.metadata_sections ~= vim.NIL
        and type(response.metadata_sections) ~= "table")
      or type(response.submitted_source) ~= "string"
      or (response.proposed_rating ~= vim.NIL and response.proposed_rating ~= nil and not RATINGS[response.proposed_rating])
    then
      set_status("solving")
      set_timing_phase("solve")
      ui.notify("Evaluation failed: invalid evaluator response", vim.log.levels.ERROR)
      return
    end

    state.result = response
    set_status("reviewing")
    set_timing_phase("feedback")
    ui.open_feedback(state.source_window, response, {
      accept = M.accept,
      accept_stay = M.accept_stay,
      rate = M.rate,
      retry = M.retry,
      skip = M.next,
      note = M.note,
      ask = M.ask,
    })
  end)
end

local function save_working_source()
  if not valid_buffer(state.source_buffer) then
    ui.notify("The practice source buffer is no longer available", vim.log.levels.ERROR)
    return false
  end
  local saved, save_error = pcall(function()
    vim.api.nvim_buf_call(state.source_buffer, function() vim.cmd("silent write") end)
  end)
  if not saved then
    ui.notify("Could not save the working copy: " .. tostring(save_error), vim.log.levels.ERROR)
    return false
  end
  return true
end

function M.give_up()
  if state.status ~= "solving" then
    ui.notify("Give up is available only while solving an exercise", vim.log.levels.WARN)
    return
  end
  if not save_working_source() then return end
  if vim.fn.confirm(
      "Give up on this exercise? This will reveal the reference and suggest a Fail rating.",
      "&Give up\n&Cancel", 2) ~= 1 then
    return
  end

  state.previous_result = nil
  state.follow_up_pending = false
  set_timing_phase("feedback")
  state.result = {
    gave_up = true,
    compiled = false,
    diagnostics = "",
    metadata = table.concat(vim.fn.readfile(state.exercise.metadata_path), "\n"),
    submitted_source = table.concat(vim.api.nvim_buf_get_lines(state.source_buffer, 0, -1, false), "\n"),
    proposed_rating = "fail",
    review = {
      status = "skipped",
      attempts = 0,
      feedback = nil,
      failure = "Compilation and reviewer assessment were skipped because you gave up.",
    },
  }
  set_status("reviewing")
  ui.open_feedback(state.source_window, state.result, {
    accept = M.accept,
    accept_stay = M.accept_stay,
    rate = M.rate,
    retry = M.retry,
    skip = M.next,
    note = M.note,
    ask = M.ask,
  })
end

local function compiler_messages(turns)
  local messages = {}
  local first = math.max(1, #turns - 7)
  for index = first, #turns do
    local turn = turns[index]
    if turn.status == "available" then
      table.insert(messages, { role = "user", content = turn.question })
      table.insert(messages, { role = "assistant", content = turn.answer })
    end
  end
  return messages
end

function M.compile()
  if state.status ~= "solving" and state.status ~= "post_rating" then
    ui.notify("Compile is available only while solving an exercise", vim.log.levels.WARN)
    return
  end
  if not save_working_source() then return end
  set_status("compiling")
  process.run(config.python, script_path("compile_exercise.py"), {
    source_path = state.working_path, command = config.evaluation_command,
  }, function(error_message, response)
    set_status("solving")
    if error_message then
      ui.open_compiler_result(state.source_window, { compiled = false, diagnostics = error_message,
        chat = { turns = {} } }, {})
      return
    end
    if type(response.compiled) ~= "boolean" or type(response.diagnostics) ~= "string"
      or type(response.submitted_source) ~= "string" or type(response.command) ~= "table" then
      ui.notify("Compile failed: invalid compiler response", vim.log.levels.ERROR)
      return
    end
    response.chat = { turns = {} }
    state.compiler_result = response
    ui.open_compiler_result(state.source_window, response, { ask = M.ask_compiler })
    ui.notify(response.compiled and "Compilation succeeded" or "Compilation has diagnostics",
      response.compiled and vim.log.levels.INFO or vim.log.levels.WARN)
  end)
end

function M.ask_compiler(question)
  local result = state.compiler_result
  if state.status ~= "solving" or not result then
    ui.notify("Compile before asking about compiler diagnostics", vim.log.levels.WARN)
    return
  end
  if state.compiler_chat_pending then
    ui.notify("Wait for the current compiler explanation", vim.log.levels.WARN)
    return
  end
  if question == nil then
    vim.ui.input({ prompt = "Ask about compiler output: " }, function(value)
      if value ~= nil then M.ask_compiler(value) end
    end)
    return
  end
  question = vim.trim(tostring(question))
  if question == "" then return end
  local turns = result.chat.turns
  local turn = { question = question, status = "pending" }
  table.insert(turns, turn)
  state.compiler_chat_pending = true
  ui.refresh_compiler_result()
  process.run(config.python, script_path("compiler_follow_up.py"), {
    evidence = { submitted_source = result.submitted_source, validation = {
      command = result.command, succeeded = result.compiled, diagnostics = result.diagnostics },
      exercise_metadata = state.exercise and table.concat(vim.fn.readfile(state.exercise.metadata_path), "\n") or "",
      target_environment = state.exercise and state.exercise.target_environment or nil },
    messages = compiler_messages(turns), question = question, reviewer = config.compiler_follow_up_reviewer,
  }, function(error_message, response)
    state.compiler_chat_pending = false
    if error_message or not response or response.status ~= "available" or type(response.answer) ~= "string" then
      turn.status, turn.failure = "failed", error_message or (response and response.failure) or "Compiler explanation unavailable"
    else
      turn.status, turn.answer = "available", response.answer
    end
    ui.refresh_compiler_result()
  end)
end

function M.zz()
  if state.status == "solving" then
    M.submit()
    return
  end
  if state.status == "selecting" or state.status == "evaluating" or state.status == "recording" then
    if confirm_exit_while_waiting() then
      vim.cmd("qa!")
    end
    return
  end
  vim.cmd("normal! ZZ")
end

local function follow_up_messages(turns)
  local messages = {}
  local first = math.max(1, #turns - 7)
  for index = first, #turns do
    local turn = turns[index]
    if turn.status == "available" then
      table.insert(messages, { role = "user", content = turn.question })
      table.insert(messages, { role = "assistant", content = turn.answer })
    end
  end
  return messages
end

function M.ask(question)
  if state.status ~= "reviewing" then
    ui.notify("A follow-up question can be asked only while reviewing feedback",
      vim.log.levels.WARN)
    return
  end
  if state.follow_up_pending then
    ui.notify("Wait for the current follow-up response", vim.log.levels.WARN)
    return
  end
  if question == nil then
    vim.ui.input({ prompt = "Ask reviewer: " }, function(value)
      if value ~= nil then M.ask(value) end
    end)
    return
  end
  question = vim.trim(tostring(question))
  if question == "" then return end

  state.result.follow_up = type(state.result.follow_up) == "table"
      and state.result.follow_up or { turns = {} }
  local turns = state.result.follow_up.turns
  local turn = {
    question = question,
    status = "pending",
    reviewer = config.follow_up_reviewer and config.follow_up_reviewer.name or "Reviewer",
    model = config.follow_up_reviewer and config.follow_up_reviewer.model or nil,
  }
  table.insert(turns, turn)
  state.follow_up_pending = true
  set_timing_phase(nil)
  ui.refresh_feedback("chat")

  process.run(config.python, script_path("review_follow_up.py"), {
    evidence = {
      starter_source = table.concat(vim.fn.readfile(state.exercise.source_path), "\n"),
      submitted_source = state.result.submitted_source,
      exercise_metadata = state.result.metadata,
      target_environment = state.exercise.target_environment,
      validation = {
        succeeded = state.result.compiled,
        diagnostics = state.result.diagnostics,
      },
    },
    initial_review = state.result.review,
    messages = follow_up_messages(turns),
    question = question,
    reviewer = config.follow_up_reviewer,
  }, function(error_message, response)
    state.follow_up_pending = false
    if error_message then
      turn.status = "failed"
      turn.failure = error_message
      ui.refresh_feedback("chat")
      ui.notify("Follow-up failed; details are shown in the feedback pane",
        vim.log.levels.ERROR)
      set_timing_phase("feedback")
      return
    end
    turn.reviewer = response.reviewer
    turn.model = response.model
    turn.reasoning_effort = response.reasoning_effort
    if response.status ~= "available" or type(response.answer) ~= "string" then
      turn.status = "failed"
      turn.failure = response.failure or "Follow-up response unavailable"
      ui.refresh_feedback("chat")
      ui.notify("Follow-up reviewer unavailable; details are shown in the feedback pane",
        vim.log.levels.WARN)
      set_timing_phase("feedback")
      return
    end
    turn.status = "available"
    turn.answer = response.answer
    ui.refresh_feedback("chat")
    set_timing_phase("feedback")
  end)
end

function M.retry()
  if state.status ~= "reviewing" then
    ui.notify("Retry is available only while reviewing feedback", vim.log.levels.WARN)
    return
  end
  if state.follow_up_pending then
    ui.notify("Wait for the current follow-up response", vim.log.levels.WARN)
    return
  end
  state.previous_result = state.result
  state.result = nil
  set_timing_phase(nil)
  ui.close_feedback()
  if valid_buffer(state.source_buffer) then
    local windows = vim.fn.win_findbuf(state.source_buffer)
    if #windows > 0 then
      state.source_window = windows[1]
      vim.api.nvim_set_current_win(state.source_window)
    elseif state.source_window and vim.api.nvim_win_is_valid(state.source_window) then
      vim.api.nvim_set_current_win(state.source_window)
      vim.api.nvim_win_set_buf(state.source_window, state.source_buffer)
    end
  end
  set_status("solving")
  set_timing_phase("solve")
  ui.notify("Returned to the unchanged source; no rating was recorded")
end

function M.rate(rating, stay)
  rating = rating and rating:lower() or nil
  if state.status ~= "reviewing" then
    ui.notify("A rating can be recorded only while reviewing feedback", vim.log.levels.WARN)
    return
  end
  if state.follow_up_pending then
    ui.notify("Wait for the current follow-up response", vim.log.levels.WARN)
    return
  end
  if not RATINGS[rating] then
    ui.notify("Unknown rating: " .. tostring(rating), vim.log.levels.ERROR)
    return
  end

  set_timing_phase(nil)
  set_status("recording")
  local record_request = {
    exercise_directory = state.collection,
    database_path = config.database_path,
    exercise_id = state.exercise.id,
    compiled = state.result.compiled,
    proposed_rating = state.result.proposed_rating,
    final_rating = rating,
    review_status = state.result.review.status,
    reviewer_name = state.result.review.reviewer,
    reviewer_model = state.result.review.model,
    reviewer_reasoning_effort = state.result.review.reasoning_effort,
    reviewer_service_tier = state.result.review.service_tier,
    reviewer_usage = state.result.review.usage,
    review_attempts = state.result.review.attempts,
    solve_duration_ms = state.timing.solve_ms,
    feedback_duration_ms = state.timing.feedback_ms,
    review_archive_ttl_days = config.review_archive_ttl_days,
  }
  if state.result.review.status ~= "skipped" then
    record_request.submitted_source = state.result.submitted_source
    record_request.review_response = state.result.review
  end
  process.run(config.python, script_path("record_rating.py"), record_request, function(error_message, response)
    if error_message then
      set_status("reviewing")
      set_timing_phase("feedback")
      ui.notify("Rating failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if response.recorded ~= true
      or type(response.due) ~= "string"
      or type(response.state) ~= "string"
    then
      set_status("reviewing")
      set_timing_phase("feedback")
      ui.notify("Rating failed: invalid recorder response", vim.log.levels.ERROR)
      return
    end
    ui.notify("Rated " .. rating:sub(1, 1):upper() .. rating:sub(2))
    statusline.invalidate(state.collections)
    sync.trigger(state.collections)
    if stay then
      state.previous_result = state.result
      state.result = nil
      ui.close_feedback()
      set_status("post_rating")
      set_timing_phase(nil)
      if valid_buffer(state.source_buffer) then vim.api.nvim_set_current_buf(state.source_buffer) end
      ui.notify("Rating recorded. You can keep experimenting; further work is ungraded.")
    else
      select_next()
    end
  end)
end

function M.accept()
  if state.status ~= "reviewing" then
    ui.notify("There is no proposed rating to accept", vim.log.levels.WARN)
    return
  end
  if type(state.result.proposed_rating) ~= "string" then
    ui.notify("No reviewer rating is available; choose a manual rating", vim.log.levels.WARN)
    return
  end
  M.rate(state.result.proposed_rating)
end

function M.accept_stay()
  if state.status ~= "reviewing" or type(state.result.proposed_rating) ~= "string" then
    ui.notify("There is no proposed rating to accept", vim.log.levels.WARN)
    return
  end
  M.rate(state.result.proposed_rating, true)
end

function M.next()
  if state.status ~= "solving" and state.status ~= "reviewing" and state.status ~= "post_rating" then
    ui.notify("Next is available only while solving or reviewing", vim.log.levels.WARN)
    return
  end
  if state.follow_up_pending then
    ui.notify("Wait for the current follow-up response", vim.log.levels.WARN)
    return
  end
  if not confirm_abandon("open the next exercise") then
    return
  end
  select_next()
end

function M.quit()
  if state.status == "idle" then
    ui.notify("No practice session is active", vim.log.levels.WARN)
    return
  end
  if state.status == "evaluating"
    or state.status == "recording"
    or state.status == "selecting"
  then
    ui.notify("Wait for the current practice operation to finish", vim.log.levels.WARN)
    return
  end
  if state.follow_up_pending then
    ui.notify("Wait for the current follow-up response", vim.log.levels.WARN)
    return
  end
  if not confirm_abandon("quit practice") then
    return
  end

  local source_window = state.source_window
  reset_session()
  if source_window and vim.api.nvim_win_is_valid(source_window) then
    vim.api.nvim_set_current_win(source_window)
    vim.cmd("enew")
  end
  ui.notify("Practice session ended")
end

function M.get_state()
  return state
end

return M
