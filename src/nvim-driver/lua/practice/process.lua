local M = {}
local log = require("practice.log")

local function invoke_callback(callback, ...)
  local arguments = { ... }
  local ok, error_message = xpcall(function()
    callback(unpack(arguments))
  end, debug.traceback)
  if not ok then
    log.event("process_callback_failed", "error", { traceback = error_message })
    error(error_message)
  end
end

local function response_summary(response)
  if type(response) ~= "table" then
    return nil
  end
  local summary = {
    error = response.error,
    compiled = response.compiled,
    proposed_rating = response.proposed_rating,
    recorded = response.recorded,
  }
  if type(response.review) == "table" then
    summary.review = {
      status = response.review.status,
      reviewer = response.review.reviewer,
      attempts = response.review.attempts,
    }
  end
  return summary
end

local function decode_response(output)
  if output == nil or output == "" then
    return nil, "script returned no JSON response"
  end

  local ok, decoded = pcall(vim.json.decode, output)
  if not ok or type(decoded) ~= "table" then
    return nil, "script returned invalid JSON"
  end
  return decoded, nil
end

function M.run(python, script, request, callback)
  local ok, input = pcall(vim.json.encode, request)
  if not ok then
    log.event("process_request_encode_failed", "error", { script = script })
    invoke_callback(callback, "could not encode script request", nil)
    return nil
  end

  local started = vim.uv.hrtime()
  log.event("process_started", "info", {
    executable = python,
    script = script,
    request_keys = vim.tbl_keys(request),
  })

  return vim.system({ python, script }, { stdin = input, text = true }, function(result)
    vim.schedule(function()
      local response, decode_error = decode_response(result.stdout)
      local duration_ms = math.floor((vim.uv.hrtime() - started) / 1000000)
      log.event("process_finished", result.code == 0 and "info" or "error", {
        executable = python,
        script = script,
        exit_code = result.code,
        signal = result.signal,
        duration_ms = duration_ms,
        stderr = result.stderr and vim.trim(result.stderr) or nil,
        decode_error = decode_error,
        response = response_summary(response),
      })
      if decode_error then
        local detail = result.stderr and vim.trim(result.stderr) or ""
        if detail ~= "" then
          decode_error = decode_error .. ": " .. detail
        end
        invoke_callback(callback, decode_error, nil)
        return
      end

      if result.code ~= 0 then
        invoke_callback(callback, response.error or ("script exited with status " .. result.code), nil)
        return
      end
      if type(response.error) == "string" then
        invoke_callback(callback, response.error, nil)
        return
      end
      invoke_callback(callback, nil, response)
    end)
  end)
end

return M
