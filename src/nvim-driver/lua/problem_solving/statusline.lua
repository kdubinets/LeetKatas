local process = require("practice.process")

local M = {}

local config = nil
local driver_config = nil
local state_provider = nil
local timer = nil
local stats = nil
local stats_collection = nil
local stats_pending = false
local stats_requested_at = 0
local refresh_again = false

local function format_duration(milliseconds)
  local seconds = math.floor(math.max(0, milliseconds) / 1000)
  if seconds < 3600 then
    return string.format("%d:%02d", math.floor(seconds / 60), seconds % 60)
  end
  return string.format("%d:%02d:%02d", math.floor(seconds / 3600),
    math.floor(seconds / 60) % 60, seconds % 60)
end

local function title_case(value)
  return value:sub(1, 1):upper() .. value:sub(2)
end

local function escape(value)
  return (tostring(value):gsub("%%", "%%%%"))
end

local function solve_elapsed(state)
  local timing = state.timing
  if type(timing) ~= "table" then return nil end
  local elapsed = timing.solve_ms or 0
  if timing.phase == "solve" and timing.started then
    elapsed = elapsed + math.max(0, math.floor((vim.uv.hrtime() - timing.started) / 1000000))
  end
  return "Solve " .. format_duration(elapsed)
end

local function item(name, state)
  local problem = state.problem
  local today = stats and stats.today
  local collection = stats and stats.collection_state
  if name == "problem_name" then
    return problem and (problem.title or problem.id) or nil
  elseif name == "problem_id" then
    return problem and problem.id or nil
  elseif name == "collection" then
    return state.collection and vim.fs.basename(state.collection) or nil
  elseif name == "phase" then
    return state.status ~= "idle" and title_case(state.status) or nil
  elseif name == "solve_elapsed" then
    return solve_elapsed(state)
  elseif name == "hint_requested" then
    return state.hint_requested and "Hint used" or nil
  elseif name == "outline_revealed" then
    return state.outline_revealed and "Outline revealed" or nil
  elseif name == "bookmarked" then
    return state.bookmarked and "Bookmarked" or nil
  elseif name == "open_bookmarks" then
    local count = state.open_bookmarks or 0
    return count > 0 and string.format("Open thoughts %d", count) or nil
  elseif name == "conversation" then
    if state.conversation_pending then return "Conversation…" end
    local count = #state.conversation_history
    return count > 0 and string.format("Messages %d", count) or nil
  elseif name == "reviews_today" then
    return today and string.format("Today %d", today.reviews) or nil
  elseif name == "new_today" then
    return today and string.format("New solved %d", today.new_reviewed) or nil
  elseif name == "new_left" then
    return collection and string.format("New left %d", collection.unseen) or nil
  elseif name == "reviews_total" then
    return stats and stats.reviews
      and string.format("Reviewed %d", stats.reviews.problems_total) or nil
  elseif name == "due_now" then
    return today and string.format("Due now %d", today.due_now) or nil
  elseif name == "due_later_today" then
    return today and string.format("Due later %d", today.due_later_today) or nil
  elseif name == "action" then
    if state.status == "solving" then return "Hint or reveal" end
    if state.status == "revealed" or state.status == "discussing" then return "Discuss or rate" end
    return nil
  end
end

function M.refresh(collection_path)
  if not config or config.enabled == false or not collection_path or stats_pending then return end
  stats_pending = true
  stats_requested_at = vim.uv.now()
  process.run(driver_config.python, driver_config.scripts_dir .. "/problem_solving_stats.py", {
    collection_directory = collection_path,
    database_path = driver_config.database_path,
  }, function(error_message, response)
    stats_pending = false
    if not error_message and type(response.today) == "table"
      and type(response.collection_state) == "table" and type(response.reviews) == "table"
    then
      stats = response
      stats_collection = collection_path
      vim.cmd("redrawstatus")
    end
    if refresh_again then
      refresh_again = false
      stats_collection = nil
      M.refresh(collection_path)
    end
  end)
end

function M.invalidate(collection_path)
  stats_collection = nil
  if stats_pending then
    refresh_again = true
  else
    M.refresh(collection_path)
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

function M.setup(options, provider)
  driver_config = options
  config = options.statusline
  state_provider = provider
  if not config or config.enabled == false then return end
  _G.ProblemSolvingStatusline = M.render
  vim.opt.laststatus = 2
  vim.opt.statusline = "%!v:lua.ProblemSolvingStatusline()"
  timer = vim.uv.new_timer()
  timer:start(1000, 1000, vim.schedule_wrap(function()
    local state = state_provider()
    if state.collection and (stats_collection ~= state.collection
      or vim.uv.now() - stats_requested_at >= 60000)
    then
      M.refresh(state.collection)
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
