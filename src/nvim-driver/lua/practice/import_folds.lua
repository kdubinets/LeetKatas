local M = {}
local spacer_namespace = vim.api.nvim_create_namespace("practice_import_fold_spacer")

-- Each entry describes the contiguous import preamble for a filetype.  Add a
-- filetype here when a new exercise language is introduced; no UI code needs
-- to change.
local language_rules = {
  c = { "^%s*#%s*include%s+" },
  cpp = { "^%s*#%s*include%s+" },
  cuda = { "^%s*#%s*include%s+" },
  objc = { "^%s*#%s*import%s+", "^%s*#%s*include%s+" },
  objcpp = { "^%s*#%s*import%s+", "^%s*#%s*include%s+" },
  python = { "^%s*import%s+[%w_]", "^%s*from%s+[%w_%.]+%s+import%s+" },
  rust = { "^%s*use%s+", "^%s*extern%s+crate%s+" },
  go = { [=[^%s*import%s*[%(\"]]=] },
  javascript = { "^%s*import%s+", "^%s*const%s+[%w_]+%s*=%s*require%s*%(" },
  javascriptreact = { "^%s*import%s+", "^%s*const%s+[%w_]+%s*=%s*require%s*%(" },
  typescript = { "^%s*import%s+", "^%s*const%s+[%w_]+%s*=%s*require%s*%(" },
  typescriptreact = { "^%s*import%s+", "^%s*const%s+[%w_]+%s*=%s*require%s*%(" },
  java = { "^%s*import%s+" },
  kotlin = { "^%s*import%s+" },
  cs = { "^%s*using%s+" },
  c_sharp = { "^%s*using%s+" },
  ruby = { "^%s*require%s*[%(\"']", "^%s*require_relative%s*[%(\"']" },
  swift = { "^%s*import%s+" },
}

local function matches(line, patterns)
  for _, pattern in ipairs(patterns) do
    if line:match(pattern) then return true end
  end
  return false
end

local function ignorable_between_imports(line)
  return line:match("^%s*$")
    or line:match("^%s*//")
    or line:match("^%s*/%*")
    or line:match("^%s*%*")
    or line:match("^%s*#%s*[^%a]")
end

local function find_import_section(lines, patterns)
  -- Imports belong in the preamble.  Do not mistake imports inside the
  -- solution body for a section to hide.
  local start_line = nil
  for index, line in ipairs(lines) do
    if matches(line, patterns) then
      start_line = index
      break
    end
    if not ignorable_between_imports(line) and not line:match("^#!") then return nil end
  end
  if not start_line then return nil end

  local finish = start_line
  for index = start_line + 1, #lines do
    if matches(lines[index], patterns) or ignorable_between_imports(lines[index]) then
      finish = index
    else
      break
    end
  end
  return start_line, finish
end

function M.close(buffer, window)
  local patterns = language_rules[vim.bo[buffer].filetype]
  if not patterns then return end

  local first, last = find_import_section(vim.api.nvim_buf_get_lines(buffer, 0, -1, false), patterns)
  if not first then return end

  local import_count = 0
  for index = first, last do
    if matches(vim.api.nvim_buf_get_lines(buffer, index - 1, index, false)[1], patterns) then
      import_count = import_count + 1
    end
  end
  vim.b[buffer].practice_import_fold_count = import_count
  vim.api.nvim_buf_clear_namespace(buffer, spacer_namespace, 0, -1)

  vim.api.nvim_win_call(window, function()
    vim.wo.foldmethod = "manual"
    vim.wo.foldenable = true
    vim.wo.foldlevel = 0
    vim.wo.foldtext = "v:lua.PracticeImportFoldText()"
    vim.cmd("silent! normal! zE")
    vim.cmd(string.format("silent! %d,%dfold", first, last))
  end)

  -- A one-import preamble needs its following blank line to form a fold.
  -- Restore that visual separation without changing the submitted source.
  if last < vim.api.nvim_buf_line_count(buffer) then
    vim.api.nvim_buf_set_extmark(buffer, spacer_namespace, last, 0, {
      virt_lines = { { { "", "Normal" } } },
      virt_lines_above = true,
    })
  end
end

function M.foldtext()
  local count = vim.b.practice_import_fold_count or 0
  local noun = count == 1 and "import" or "imports"
  return string.format("  %d %s hidden", count, noun)
end

_G.PracticeImportFoldText = M.foldtext

return M
