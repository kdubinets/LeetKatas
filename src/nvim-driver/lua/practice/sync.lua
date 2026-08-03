local process = require("practice.process")
local log = require("practice.log")

local M = {}
local config = nil
local running = false
local last = {
  configured = false,
  status = "disabled",
  pending = 0,
  last_success = nil,
}

local function request(action, directory, manual, callback)
  if running then
    if manual then
      vim.notify("Practice synchronization is already running", vim.log.levels.WARN,
        { title = "Practice Sync" })
    end
    return false
  end
  if action ~= "status" and not config.supabase_url then
    last = { configured = false, status = "disabled", pending = last.pending or 0 }
    if manual then
      vim.notify("Practice synchronization is disabled", vim.log.levels.INFO,
        { title = "Practice Sync" })
    end
    if callback then callback(last) end
    return false
  end

  running = true
  process.run(config.python, config.scripts_dir .. "/sync_progress.py", {
    action = action,
    exercise_directory = directory or config.default_directory,
    database_path = config.database_path,
    supabase_url = config.supabase_url,
  }, function(error_message, response)
    running = false
    if error_message then
      log.event("sync_process_failed", "error", { error = error_message })
      response = {
        configured = config.supabase_url ~= nil,
        status = "unavailable",
        pending = last.pending or 0,
      }
    end
    last = vim.tbl_extend("force", last, response)
    log.event("sync_finished", response.status == "success" and "info" or "warn", {
      status = response.status,
      uploaded = response.uploaded,
      downloaded = response.downloaded,
      pending = response.pending,
      error = response.error,
    })
    if manual then
      if response.status == "success" then
        vim.notify(string.format("Synchronized: %d uploaded, %d downloaded",
          response.uploaded or 0, response.downloaded or 0), vim.log.levels.INFO,
          { title = "Practice Sync" })
      elseif response.status == "bootstrap_conflict" then
        vim.notify("Synchronization stopped: bootstrap conflict; local and remote history were preserved",
          vim.log.levels.ERROR, { title = "Practice Sync" })
      elseif response.status == "disabled" then
        vim.notify("Practice synchronization is disabled", vim.log.levels.INFO,
          { title = "Practice Sync" })
      else
        vim.notify(string.format("Synchronization unavailable; %d local event(s) pending",
          response.pending or 0), vim.log.levels.WARN, { title = "Practice Sync" })
      end
    end
    if callback then callback(last) end
  end)
  return true
end

function M.setup(options)
  config = options
  vim.schedule(function() M.trigger(options.default_directory) end)
end

function M.trigger(directory)
  return request("sync", directory, false)
end

function M.manual(directory)
  return request("sync", directory, true)
end

function M.diagnostics(directory, callback)
  if running then
    callback(last)
    return
  end
  request("status", directory, false, callback)
end

function M.get_state()
  return last
end

return M
