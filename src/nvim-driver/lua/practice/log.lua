local M = {}

local log_path = nil
local session_id = nil

local function timestamp()
  return os.date("!%Y-%m-%dT%H:%M:%SZ")
end

local function sanitize(value, depth)
  if depth > 4 then
    return "<truncated>"
  end
  if value == vim.NIL then
    return nil
  end
  if type(value) ~= "table" then
    return value
  end
  local result = {}
  for key, item in pairs(value) do
    result[key] = sanitize(item, depth + 1)
  end
  return result
end

function M.setup(path)
  log_path = vim.fn.fnamemodify(path, ":p")
  session_id = string.format("%s-%d", os.date("!%Y%m%dT%H%M%SZ"), vim.fn.getpid())
  vim.fn.mkdir(vim.fn.fnamemodify(log_path, ":h"), "p")
  local size = vim.fn.getfsize(log_path)
  if size > 2 * 1024 * 1024 then
    local previous = log_path .. ".1"
    vim.fn.delete(previous)
    vim.uv.fs_rename(log_path, previous)
  end
  M.event("session_started", "info", {
    nvim = vim.version().major .. "." .. vim.version().minor .. "." .. vim.version().patch,
  })
end

function M.event(name, level, fields)
  if not log_path then
    return
  end
  local entry = sanitize(fields or {}, 0)
  entry.timestamp = timestamp()
  entry.session_id = session_id
  entry.event = name
  entry.level = level or "info"
  local ok, encoded = pcall(vim.json.encode, entry)
  if ok then
    pcall(vim.fn.writefile, { encoded }, log_path, "a")
  end
end

function M.path()
  return log_path
end

function M.session_id()
  return session_id
end

function M.open()
  if not log_path then
    return
  end
  vim.cmd("tabnew " .. vim.fn.fnameescape(log_path))
  vim.bo.readonly = true
  vim.bo.modifiable = false
end

return M
