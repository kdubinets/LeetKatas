local M = {}

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
    callback("could not encode script request", nil)
    return nil
  end

  return vim.system({ python, script }, { stdin = input, text = true }, function(result)
    vim.schedule(function()
      local response, decode_error = decode_response(result.stdout)
      if decode_error then
        local detail = result.stderr and vim.trim(result.stderr) or ""
        if detail ~= "" then
          decode_error = decode_error .. ": " .. detail
        end
        callback(decode_error, nil)
        return
      end

      if result.code ~= 0 then
        callback(response.error or ("script exited with status " .. result.code), nil)
        return
      end
      if type(response.error) == "string" then
        callback(response.error, nil)
        return
      end
      callback(nil, response)
    end)
  end)
end

return M
