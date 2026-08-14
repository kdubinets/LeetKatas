local process = require("practice.process")

local M = {}

local config = nil
local driver_config = nil
local state_provider = nil
local stats = nil
local stats_collection = nil
local stats_pending = false
local stats_requested_at = 0
local timer = nil
local refresh_again = false

local function valid_buffer(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
end

local function title_case(value)
  return value:sub(1, 1):upper() .. value:sub(2)
end

local function format_duration(milliseconds)
  local seconds = math.floor(math.max(0, milliseconds) / 1000)
  if seconds < 3600 then
    return string.format("%d:%02d", math.floor(seconds / 60), seconds % 60)
  end
  return string.format("%d:%02d:%02d", math.floor(seconds / 3600),
    math.floor(seconds / 60) % 60, seconds % 60)
end

local function current_timing_ms(state)
  local timing = state.timing
  if type(timing) ~= "table" then return 0 end
  local total = (timing.solve_ms or 0) + (timing.feedback_ms or 0)
  if timing.started then
    total = total + math.max(0, math.floor((vim.uv.hrtime() - timing.started) / 1000000))
  end
  return total
end

local function escape(value)
  return (tostring(value):gsub("%%", "%%%%"))
end

local function language(exercise)
  local environment = exercise and exercise.target_environment
  local details = type(environment) == "table" and environment.language or nil
  if type(details) ~= "table" then return nil end
  if type(details.version) == "string" and details.version ~= "" then
    return details.version
  end
  return type(details.name) == "string" and details.name or nil
end

local function active_window()
  local window = tonumber(vim.g.statusline_winid)
  return window and vim.api.nvim_win_is_valid(window) and window or vim.api.nvim_get_current_win()
end

local function item(name, state)
  local exercise = state.exercise
  local today = stats and stats.today
  local collection = stats and stats.collection_state
  if name == "exercise_name" then
    return exercise and (exercise.name or exercise.id) or nil
  elseif name == "exercise_id" then
    return exercise and exercise.id or nil
  elseif name == "collection" then
    return state.collection and vim.fs.basename(state.collection) or nil
  elseif name == "phase" then
    return state.status ~= "idle" and title_case(state.status) or nil
  elseif name == "phase_elapsed" then
    if not state.timing or not state.timing.phase then return nil end
    local elapsed = state.timing[state.timing.phase .. "_ms"] or 0
    if state.timing.started then
      elapsed = elapsed + math.max(0,
        math.floor((vim.uv.hrtime() - state.timing.started) / 1000000))
    end
    return format_duration(elapsed)
  elseif name == "solve_elapsed" then
    if not state.timing then return nil end
    local elapsed = state.timing.solve_ms or 0
    if state.timing.phase == "solve" and state.timing.started then
      elapsed = elapsed + math.max(0,
        math.floor((vim.uv.hrtime() - state.timing.started) / 1000000))
    end
    return "Solve " .. format_duration(elapsed)
  elseif name == "language" then
    return language(exercise)
  elseif name == "modified" then
    return valid_buffer(state.source_buffer) and vim.bo[state.source_buffer].modified and "[+]" or nil
  elseif name == "position" then
    local window = active_window()
    local cursor = vim.api.nvim_win_get_cursor(window)
    return string.format("%d:%d", cursor[1], cursor[2] + 1)
  elseif name == "compile_result" then
    return state.result and (state.result.compiled and "Compile ✓" or "Compile ✗") or nil
  elseif name == "proposed_rating" then
    local rating = state.result and state.result.proposed_rating
    return type(rating) == "string" and ("Suggested " .. title_case(rating)) or nil
  elseif name == "progress" then
    local event = state.progress_events and state.progress_events[#state.progress_events]
    return event and (event.message or event.stage or event.status) or nil
  elseif name == "action" then
    if state.status == "solving" then return "ZZ Submit (5s)" end
    if state.status == "reviewing" then return "Accept or rate" end
    return nil
  elseif name == "time_today" then
    return today and ("Today " .. format_duration(today.practice_time_ms + current_timing_ms(state))) or nil
  elseif name == "reviews_today" then
    return today and string.format("Solved %d", today.reviews) or nil
  elseif name == "due_now" then
    return today and string.format("Due now %d", today.due_now) or nil
  elseif name == "due_later_today" then
    return today and string.format("Due later %d", today.due_later_today) or nil
  elseif name == "new_today" then
    return today and string.format("New today %d", today.new_introduced) or nil
  elseif name == "new_left" then
    return collection and string.format("New left %d", collection.unseen) or nil
  elseif name == "collection_progress" then
    return collection and string.format("Seen %d/%d", collection.introduced, collection.total) or nil
  elseif name == "tomorrow_due" then
    return stats and stats.forecast
      and string.format("Due tomorrow %d", stats.forecast.tomorrow_due)
      or nil
  end
end

local function render_items(names, state)
  local values = {}
  for _, name in ipairs(names) do
    local value = item(name, state)
    if value ~= nil and value ~= "" then table.insert(values, escape(value)) end
  end
  return table.concat(values, escape(config.separator))
end

function M.render()
  if not config or config.enabled == false or not state_provider then return "" end
  local state = state_provider()
  local left = render_items(config.left, state)
  local right = render_items(config.right, state)
  if left ~= "" and right ~= "" then return " " .. left .. "%=" .. right .. " " end
  if left ~= "" then return " " .. left .. " " end
  if right ~= "" then return "%=" .. right .. " " end
  return ""
end

function M.refresh(collections)
  if not config or config.enabled == false or type(collections) ~= "table" or stats_pending then return end
  stats_pending = true
  stats_requested_at = vim.uv.now()
  process.run(driver_config.python, driver_config.scripts_dir .. "/practice_stats.py", {
    exercise_directories = collections,
    database_path = driver_config.database_path,
    source_extension = driver_config.source_extension,
    metadata_extension = driver_config.metadata_extension,
    history_days = 1,
  }, function(error_message, response)
    stats_pending = false
    if not error_message and type(response.today) == "table"
      and type(response.collection_state) == "table" and type(response.forecast) == "table"
    then
      stats = response
      stats_collection = vim.json.encode(collections)
      vim.cmd("redrawstatus")
    end
    if refresh_again then
      refresh_again = false
      stats_collection = nil
      M.refresh(collections)
    end
  end)
end

function M.invalidate(collections)
  stats_collection = nil
  if stats_pending then
    refresh_again = true
  else
    M.refresh(collections)
  end
end

function M.setup(options, provider)
  driver_config = options
  config = options.statusline
  state_provider = provider
  if not config or config.enabled == false then return end
  _G.PracticeStatusline = M.render
  vim.opt.laststatus = 2
  vim.opt.statusline = "%!v:lua.PracticeStatusline()"
  timer = vim.uv.new_timer()
  timer:start(1000, 1000, vim.schedule_wrap(function()
    if not state_provider then return end
    local state = state_provider()
    if state.collections and (stats_collection ~= vim.json.encode(state.collections)
      or vim.uv.now() - stats_requested_at >= 60000)
    then
      M.refresh(state.collections)
    end
    vim.cmd("redrawstatus")
  end))
end

function M.stop()
  if timer then
    timer:stop()
    timer:close()
    timer = nil
  end
end

return M
