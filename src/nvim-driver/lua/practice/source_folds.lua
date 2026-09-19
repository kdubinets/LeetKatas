local M = {}
local imports = require("practice.import_folds")
local spacer_namespace = vim.api.nvim_create_namespace("practice_source_fold_spacer")

local function is_hint(line)
  return line:match("^%s*//%s*Pattern:%s*%S") ~= nil
end

local function section(buffer, kind)
  if kind == "imports" then return imports.section(buffer) end
  local lines = vim.api.nvim_buf_get_lines(buffer, 0, -1, false)
  for index, line in ipairs(lines) do
    if is_hint(line) then
      -- Include only the optional spacer, never the task or supporting code.
      local last = lines[index + 1] and lines[index + 1]:match("^%s*$")
        and index + 1 or index
      return index, last, 1
    end
  end
end

function M.has_hint(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
    and section(buffer, "hint") ~= nil
end

local function configure()
  if vim.wo.foldmethod ~= "manual" then vim.wo.foldmethod = "manual" end
  vim.wo.foldenable = true
  vim.wo.foldminlines = 0
  vim.wo.foldtext = "v:lua.PracticeSourceFoldText()"
end

function M.close(buffer, window, kind)
  local first, last, count = section(buffer, kind)
  if not first then return nil end
  if kind == "imports" then
    vim.b[buffer].practice_import_fold_count = count
    vim.api.nvim_buf_clear_namespace(buffer, spacer_namespace, 0, -1)
    -- Restore the blank separator consumed by the import fold.
    local lines = vim.api.nvim_buf_get_lines(buffer, 0, -1, false)
    if last < #lines and lines[last]:match("^%s*$") then
      vim.api.nvim_buf_set_extmark(buffer, spacer_namespace, last, 0, {
        virt_lines = { { { "", "Normal" } } },
        virt_lines_above = true,
      })
    end
  end
  vim.api.nvim_win_call(window, function()
    local cursor = vim.api.nvim_win_get_cursor(window)
    configure()
    if vim.fn.foldlevel(first) == 0 then
      vim.cmd(string.format("silent! %d,%dfold", first, last))
    end
    vim.api.nvim_win_set_cursor(window, { first, 0 })
    vim.cmd("silent! normal! zc")
    vim.api.nvim_win_set_cursor(window, cursor)
  end)
  return count
end

function M.initialize(buffer, window)
  vim.api.nvim_buf_clear_namespace(buffer, spacer_namespace, 0, -1)
  vim.api.nvim_win_call(window, function()
    configure()
    vim.wo.foldlevel = 0
    vim.cmd("silent! normal! zE")
  end)
  M.close(buffer, window, "imports")
  M.close(buffer, window, "hint")
end

function M.toggle(buffer, window, kind)
  local first, _, count = section(buffer, kind)
  if not first then return nil end
  if vim.api.nvim_win_call(window, function() return vim.fn.foldclosed(first) >= 0 end) then
    vim.api.nvim_win_call(window, function()
      local cursor = vim.api.nvim_win_get_cursor(window)
      vim.api.nvim_win_set_cursor(window, { first, 0 })
      vim.cmd("silent! normal! zo")
      vim.api.nvim_win_set_cursor(window, cursor)
    end)
    return count, true
  end
  return M.close(buffer, window, kind), false
end

function M.foldtext()
  local buffer = vim.api.nvim_get_current_buf()
  local first, last = vim.v.foldstart, vim.v.foldend
  -- Edits at a fold boundary can move its marker without moving its start.
  local hint_first = section(buffer, "hint")
  if hint_first and first <= hint_first and hint_first <= last then
    return "  Hint hidden — <Space>h to reveal"
  end
  local import_first = imports.section(buffer)
  if import_first and first <= import_first and import_first <= last then
    return imports.foldtext()
  end
  return "  Source hidden"
end

_G.PracticeSourceFoldText = M.foldtext

return M
