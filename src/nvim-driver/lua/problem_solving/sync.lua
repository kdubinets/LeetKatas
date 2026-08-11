local process = require("practice.process")
local log = require("practice.log")

local M = {}
local config, running = nil, false
local last = { configured = false, status = "disabled", pending = {} }

local function pending_count(pending)
  if type(pending) ~= "table" then return 0 end
  return (pending.reviews or 0) + (pending.bookmarks or 0) + (pending.artifacts or 0)
end

local function body(action, directory)
  return {
    action = action,
    collection_directory = directory or config.default_directory,
    database_path = config.database_path,
    supabase_url = config.supabase_url,
    private_content_sync = config.private_content_sync,
  }
end

local function apply(response)
  last = vim.tbl_extend("force", last, response)
  log.event("problem_solving_sync_finished", response.status == "success" and "info" or "warn", {
    status = response.status,
    uploaded = response.uploaded,
    downloaded = response.downloaded,
    pending = response.pending,
    error = response.error,
  })
  return last
end

local function request(action, directory, manual, callback)
  if running then
    if manual then vim.notify("Problem-solving synchronization is already running") end
    return false
  end
  running = true
  process.run(config.python, config.scripts_dir .. "/sync_problem_solving.py",
    body(action, directory), function(error_message, response)
      running = false
      if error_message then
        response = { configured = config.supabase_url ~= nil, status = "unavailable",
          pending = last.pending or {} }
      end
      apply(response)
      if manual then
        if response.status == "success" then
          vim.notify("Problem-solving history synchronized", vim.log.levels.INFO,
            { title = "Problem Solving Sync" })
        elseif response.status == "disabled" then
          vim.notify("Problem-solving synchronization is disabled", vim.log.levels.INFO,
            { title = "Problem Solving Sync" })
        else
          vim.notify(string.format("Synchronization unavailable; %d item(s) pending",
            pending_count(response.pending)), vim.log.levels.WARN,
            { title = "Problem Solving Sync" })
        end
      end
      if callback then callback(last) end
    end)
  return true
end

function M.setup(options)
  config = options
  if not config.sync_first then vim.schedule(function() M.trigger(options.default_directory) end) end
end

function M.sync_first(directory)
  if not config.supabase_url then return apply({ configured = false, status = "disabled" }) end
  local result = vim.system(
    { config.python, config.scripts_dir .. "/sync_problem_solving.py" },
    { stdin = vim.json.encode(body("sync", directory)), text = true }
  ):wait()
  local ok, response = pcall(vim.json.decode, result.stdout or "")
  if result.code ~= 0 or not ok or type(response) ~= "table" then
    return apply({ configured = true, status = "unavailable", pending = last.pending or {} })
  end
  return apply(response)
end

function M.trigger(directory) return request("sync", directory, false) end
function M.manual(directory) return request("sync", directory, true) end
function M.diagnostics(directory, callback) return request("status", directory, false, callback) end
function M.get_state() return last end

return M
