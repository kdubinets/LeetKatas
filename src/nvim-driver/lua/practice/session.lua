local process = require("practice.process")
local ui = require("practice.ui")
local log = require("practice.log")
local notes = require("practice.notes")

local M = {}

local RATINGS = {
  fail = true,
  acceptable = true,
  good = true,
  excellent = true,
}

local state = {
  status = "idle",
  collection = nil,
  previous_id = nil,
  exercise = nil,
  result = nil,
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
}

local config = nil

local function valid_buffer(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
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
  ui.open_progress(state.source_window)
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
end

local function delete_working_copy()
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
  state.working_path = nil
  state.source_buffer = nil
  state.next_due = nil
  state.progress_path = nil
  state.progress_events = {}
  state.progress_event_count = 0
end

local function reset_session()
  delete_working_copy()
  if state.session_directory then
    vim.fn.delete(state.session_directory, "rf")
  end
  state.status = "idle"
  state.collection = nil
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
    and type(exercise.source_path) == "string"
    and type(exercise.metadata_path) == "string"
end

local function open_selected_exercise(exercise)
  if not ensure_session_directory() then
    state.status = "idle"
    return
  end

  local working_path = state.session_directory .. "/" .. vim.fs.basename(exercise.source_path)
  local copied, copy_error = vim.uv.fs_copyfile(exercise.source_path, working_path)
  if not copied then
    state.status = "idle"
    ui.notify("Could not create working copy: " .. tostring(copy_error), vim.log.levels.ERROR)
    return
  end

  state.exercise = exercise
  state.previous_id = exercise.id
  state.working_path = working_path
  state.source_buffer, state.source_window = ui.open_source(
    working_path,
    state.source_window,
    config.practice_marker
  )
  state.status = "solving"
  ui.notify("Exercise: " .. exercise.id)
end

local function select_next()
  delete_working_copy()
  state.status = "selecting"
  process.run(config.python, script_path("select_exercise.py"), {
    exercise_directory = state.collection,
    database_path = config.database_path,
    source_extension = config.source_extension,
    metadata_extension = config.metadata_extension,
    previous_exercise_id = state.previous_id,
  }, function(error_message, response)
    if error_message then
      state.status = "idle"
      ui.notify("Selection failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if (response.exercise == nil or response.exercise == vim.NIL)
      and type(response.next_due) == "string"
    then
      state.status = "complete"
      state.next_due = response.next_due
      ui.notify("No exercises are due. Next review: " .. response.next_due)
      return
    end
    if not valid_exercise(response.exercise) then
      state.status = "idle"
      ui.notify("Selection failed: invalid exercise response", vim.log.levels.ERROR)
      return
    end
    open_selected_exercise(response.exercise)
  end)
end

function M.setup(options)
  config = options
  notes.setup(options)
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
    and state.status ~= "reviewing"
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

function M.start(directory)
  if state.status == "selecting"
    or state.status == "evaluating"
    or state.status == "recording"
  then
    ui.notify("Wait for the current practice operation to finish", vim.log.levels.WARN)
    return
  end
  if state.status ~= "idle" and not confirm_abandon("restart practice") then
    return
  end
  reset_session()
  state.collection = directory and vim.fn.fnamemodify(directory, ":p") or config.default_directory
  select_next()
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

  state.status = "evaluating"
  start_progress()
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
    if error_message then
      state.status = "solving"
      ui.show_progress_error(error_message)
      ui.notify("Evaluation failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if type(response.compiled) ~= "boolean"
      or type(response.diagnostics) ~= "string"
      or type(response.metadata) ~= "string"
      or (response.proposed_rating ~= vim.NIL and response.proposed_rating ~= nil and not RATINGS[response.proposed_rating])
    then
      state.status = "solving"
      ui.notify("Evaluation failed: invalid evaluator response", vim.log.levels.ERROR)
      return
    end

    state.result = response
    state.status = "reviewing"
    ui.open_feedback(state.source_window, response)
  end)
end

function M.rate(rating)
  rating = rating and rating:lower() or nil
  if state.status ~= "reviewing" then
    ui.notify("A rating can be recorded only while reviewing feedback", vim.log.levels.WARN)
    return
  end
  if not RATINGS[rating] then
    ui.notify("Unknown rating: " .. tostring(rating), vim.log.levels.ERROR)
    return
  end

  state.status = "recording"
  process.run(config.python, script_path("record_rating.py"), {
    exercise_directory = state.collection,
    database_path = config.database_path,
    exercise_id = state.exercise.id,
    compiled = state.result.compiled,
    proposed_rating = state.result.proposed_rating,
    final_rating = rating,
    review_status = state.result.review.status,
    reviewer_name = state.result.review.reviewer,
    review_attempts = state.result.review.attempts,
  }, function(error_message, response)
    if error_message then
      state.status = "reviewing"
      ui.notify("Rating failed: " .. error_message, vim.log.levels.ERROR)
      return
    end
    if response.recorded ~= true
      or type(response.due) ~= "string"
      or type(response.state) ~= "string"
    then
      state.status = "reviewing"
      ui.notify("Rating failed: invalid recorder response", vim.log.levels.ERROR)
      return
    end
    ui.notify("Rated " .. rating:sub(1, 1):upper() .. rating:sub(2))
    select_next()
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

function M.next()
  if state.status ~= "solving" and state.status ~= "reviewing" then
    ui.notify("Next is available only while solving or reviewing", vim.log.levels.WARN)
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
