local M = {}

-- Each entry describes the contiguous import preamble for a filetype.  Add a
-- filetype here when a new exercise language is introduced; no UI code needs
-- to change.
local language_rules = {
  c = { "^%s*#%s*include%s+" },
  cpp = { "^%s*#%s*include%s+", "^%s*using%s+namespace%s+std%s*;%s*$" },
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

-- A C++ using-directive belongs to the folded preamble but is not itself an
-- import, so keep the fold label's include count accurate.
local import_count_rules = {
  cpp = { "^%s*#%s*include%s+" },
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
    -- A hint is a separate section, even when it follows the imports.
    if lines[index]:match("^%s*//%s*Pattern:") then break end
    if matches(lines[index], patterns) or ignorable_between_imports(lines[index]) then
      finish = index
    else
      break
    end
  end
  return start_line, finish
end

function M.section(buffer)
  local patterns = language_rules[vim.bo[buffer].filetype]
  if not patterns then return nil end

  local first, last = find_import_section(vim.api.nvim_buf_get_lines(buffer, 0, -1, false), patterns)
  if not first then return nil end

  local import_count = 0
  local count_patterns = import_count_rules[vim.bo[buffer].filetype] or patterns
  for index = first, last do
    if matches(vim.api.nvim_buf_get_lines(buffer, index - 1, index, false)[1], count_patterns) then
      import_count = import_count + 1
    end
  end
  return first, last, import_count
end

function M.close(buffer, window)
  return require("practice.source_folds").close(buffer, window, "imports")
end

function M.toggle(buffer, window)
  return require("practice.source_folds").toggle(buffer, window, "imports")
end

function M.foldtext()
  local count = vim.b.practice_import_fold_count or 0
  local noun = count == 1 and "import" or "imports"
  return string.format("  %d %s hidden", count, noun)
end

_G.PracticeImportFoldText = M.foldtext

return M
