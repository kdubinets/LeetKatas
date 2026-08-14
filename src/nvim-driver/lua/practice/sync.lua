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

local function apply_response(response)
  last = vim.tbl_extend("force", last, response)
  log.event("sync_finished", response.status == "success" and "info" or "warn", {
    status = response.status,
    uploaded = response.uploaded,
    downloaded = response.downloaded,
    pending = response.pending,
    error = response.error,
  })
  return last
end

local function request(action, directory, manual, callback)
  if type(directory) == "table" then
    if #directory == 0 then return false end
    if #directory == 1 then
      directory = directory[1]
    else
      local index, responses = 1, {}
      local function next_request()
        if index > #directory then
          local summary = { configured = config.supabase_url ~= nil, status = "success",
            uploaded = 0, downloaded = 0, pending = 0, collections = responses }
          for _, response in ipairs(responses) do
            summary.uploaded = summary.uploaded + (response.uploaded or 0)
            summary.downloaded = summary.downloaded + (response.downloaded or 0)
            summary.pending = summary.pending + (response.pending or 0)
            if response.status ~= "success" then summary.status = response.status end
          end
          last = summary
          if manual then
            vim.notify(string.format("Synchronized %d collection(s): %d uploaded, %d downloaded",
              #responses, summary.uploaded, summary.downloaded), vim.log.levels.INFO,
              { title = "Practice Sync" })
          end
          if callback then callback(last) end
          return
        end
        local current = directory[index]
        index = index + 1
        request(action, current, false, function(response)
          table.insert(responses, response)
          next_request()
        end)
      end
      next_request()
      return true
    end
  end
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
    apply_response(response)
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
  if not config.sync_first then
    vim.schedule(function() M.trigger(options.default_directories) end)
  end
end

-- Run before first selection when requested by the launcher. This uses the
-- normal sync JSON protocol, but waits so downloaded cards are ready to select.
function M.sync_first(directory)
  if running then return last end
  if not config.supabase_url then
    return apply_response({ configured = false, status = "disabled", pending = last.pending or 0 })
  end
  directory = directory or config.default_directories
  if type(directory) == "table" then
    local summary = { configured = true, status = "success", uploaded = 0, downloaded = 0,
      pending = 0, collections = {} }
    for _, item in ipairs(directory) do
      local response = M.sync_first(item)
      table.insert(summary.collections, response)
      summary.uploaded = summary.uploaded + (response.uploaded or 0)
      summary.downloaded = summary.downloaded + (response.downloaded or 0)
      summary.pending = summary.pending + (response.pending or 0)
      if response.status ~= "success" then summary.status = response.status end
    end
    return apply_response(summary)
  end

  local request_body = {
    action = "sync",
    exercise_directory = directory,
    database_path = config.database_path,
    supabase_url = config.supabase_url,
  }
  local encoded, input = pcall(vim.json.encode, request_body)
  if not encoded then
    return apply_response({ configured = true, status = "unavailable", pending = last.pending or 0,
      error = "could not encode sync request" })
  end

  local script = config.scripts_dir .. "/sync_progress.py"
  log.event("sync_process_started", "info", {
    executable = config.python,
    script = script,
    synchronous = true,
  })
  local started = vim.uv.hrtime()
  local result = vim.system({ config.python, script }, { stdin = input, text = true }):wait()
  local duration_ms = math.floor((vim.uv.hrtime() - started) / 1000000)
  local decoded, response = pcall(vim.json.decode, result.stdout or "")
  if not decoded or type(response) ~= "table" then
    local error_message = "script returned invalid JSON"
    if result.stderr and vim.trim(result.stderr) ~= "" then
      error_message = error_message .. ": " .. vim.trim(result.stderr)
    end
    log.event("sync_process_finished", "error", {
      exit_code = result.code, signal = result.signal, duration_ms = duration_ms,
      error = error_message,
    })
    return apply_response({ configured = true, status = "unavailable", pending = last.pending or 0,
      error = error_message })
  end
  log.event("sync_process_finished", result.code == 0 and "info" or "error", {
    exit_code = result.code, signal = result.signal, duration_ms = duration_ms,
    error = response.error,
  })
  if result.code ~= 0 then
    response = {
      configured = true, status = "unavailable", pending = last.pending or 0,
      error = response.error or ("script exited with status " .. result.code),
    }
  end
  return apply_response(response)
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
