local init_path = debug.getinfo(1, "S").source:sub(2)
local driver_dir = vim.fn.fnamemodify(init_path, ":p:h")
local repository_dir = vim.fn.fnamemodify(driver_dir, ":h:h")

vim.g.mapleader = " "
vim.g.maplocalleader = " "
vim.opt.loadplugins = false
vim.opt.swapfile = false
vim.opt.termguicolors = true
vim.cmd("filetype on")
vim.cmd("syntax enable")

package.path = table.concat({
  driver_dir .. "/lua/?.lua",
  driver_dir .. "/lua/?/init.lua",
  package.path,
}, ";")

local function environment(name)
  local value = vim.env[name]
  return value ~= nil and value ~= "" and value or nil
end

local python = environment("PRACTICE_PYTHON")
  or (vim.fn.executable(repository_dir .. "/.venv/bin/python") == 1
    and repository_dir .. "/.venv/bin/python" or "python3")

local config_root = environment("XDG_CONFIG_HOME") or vim.fn.expand("~/.config")
local config_path = environment("PROBLEM_SOLVING_CONFIG")
  or config_root .. "/leetkatas/problem-solving.toml"
local output = vim.fn.system(
  { python, repository_dir .. "/src/scripts/load_practice_config.py" },
  vim.json.encode({ path = config_path })
)
local ok, response = pcall(vim.json.decode, output)
if vim.v.shell_error ~= 0 or not ok or type(response) ~= "table" or response.error then
  local detail = ok and type(response) == "table" and response.error or output
  error("Invalid problem-solving configuration: " .. tostring(detail))
end

local configured = (response.config or {}).problem_solving or {}
local reviewer_config = (response.config or {}).reviewer or {}
local editor_config = (response.config or {}).editor or {}
local statusline_config = (response.config or {}).statusline or {}
local data_root = environment("XDG_DATA_HOME") or vim.fn.expand("~/.local/share")
local state_root = environment("XDG_STATE_HOME") or vim.fn.expand("~/.local/state")

local function setup_which_key(delay)
  local plugin_dir = vim.fn.stdpath("data") .. "/leetkatas/which-key.nvim"
  if vim.fn.isdirectory(plugin_dir) == 0 and vim.env.PRACTICE_INSTALL_PLUGINS == "1" then
    local install = vim.fn.confirm(
      "Problem-solving practice can download and run which-key.nvim v3.17.0 from GitHub. Install it?",
      "&Install\n&Skip",
      2
    )
    if install ~= 1 then
      return
    end
    vim.fn.mkdir(vim.fn.fnamemodify(plugin_dir, ":h"), "p")
    local install_output = vim.fn.system({
      "git", "clone", "--filter=blob:none", "--branch=v3.17.0", "--single-branch",
      "https://github.com/folke/which-key.nvim.git", plugin_dir,
    })
    if vim.v.shell_error ~= 0 then
      vim.schedule(function()
        vim.notify("Could not install which-key.nvim:\n" .. install_output,
          vim.log.levels.WARN, { title = "Problem Solving" })
      end)
      return
    end
  end
  if vim.fn.isdirectory(plugin_dir) == 0 then
    return
  end

  vim.opt.runtimepath:prepend(plugin_dir)
  local loaded, which_key = pcall(require, "which-key")
  if loaded then
    which_key.setup({ delay = delay })
  else
    vim.schedule(function()
      vim.notify("The cached which-key.nvim plugin could not be loaded.",
        vim.log.levels.WARN, { title = "Problem Solving" })
    end)
  end
end

setup_which_key(editor_config.which_key_delay_ms or 300)

local private_sync_override = environment("PROBLEM_SOLVING_PRIVATE_CONTENT_SYNC")
if private_sync_override and private_sync_override ~= "0" and private_sync_override ~= "1" then
  error("PROBLEM_SOLVING_PRIVATE_CONTENT_SYNC must be 0 or 1")
end
local retain_history_override = environment("PROBLEM_SOLVING_RETAIN_CONVERSATION_HISTORY")
if retain_history_override and retain_history_override ~= "0" and retain_history_override ~= "1" then
  error("PROBLEM_SOLVING_RETAIN_CONVERSATION_HISTORY must be 0 or 1")
end
local reviewer_model = environment("PROBLEM_SOLVING_REVIEW_MODEL")
  or reviewer_config.model or "gpt-5.6-luna"
local reviewer_effort = environment("PROBLEM_SOLVING_REVIEW_EFFORT")
  or reviewer_config.reasoning_effort or "low"
local reviewer_override = environment("PROBLEM_SOLVING_REVIEWER")
local function conversation_reviewer(mode)
  if reviewer_override then
    return {
      command = { reviewer_override },
      name = environment("PROBLEM_SOLVING_REVIEWER_NAME") or "Level C reviewer",
      model = reviewer_model,
      reasoning_effort = reviewer_effort,
    }
  end
  return {
    command = {
      python, repository_dir .. "/src/scripts/level_c_codex.py",
      "--mode", mode, "--model", reviewer_model, "--effort", reviewer_effort,
    },
    name = "Codex",
    model = reviewer_model,
    reasoning_effort = reviewer_effort,
  }
end
local problem_solving = require("problem_solving")
problem_solving.setup({
  python = python,
  scripts_dir = repository_dir .. "/src/scripts",
  default_directory = environment("PROBLEM_SOLVING_COLLECTION") or configured.collection
    or repository_dir .. "/practice/problem_solving/collections/initial_seed",
  database_path = environment("PROBLEM_SOLVING_DATABASE") or configured.database_path,
  log_path = environment("PROBLEM_SOLVING_LOG") or configured.log_path
    or state_root .. "/leetkatas/problem-solving.log",
  notes_directory = environment("PROBLEM_SOLVING_NOTES_DIRECTORY")
    or configured.notes_directory or data_root .. "/leetkatas/problem-solving-notes",
  supabase_url = environment("PROBLEM_SOLVING_SUPABASE_URL") or configured.supabase_url,
  private_content_sync = private_sync_override == "1"
    or (private_sync_override == nil and configured.private_content_sync == true),
  retain_conversation_history = retain_history_override == "1"
    or (retain_history_override == nil and configured.retain_conversation_history ~= false),
  clarification_reviewer = conversation_reviewer("clarification"),
  discussion_reviewer = conversation_reviewer("discussion"),
  sync_first = vim.env.PROBLEM_SOLVING_SYNC_FIRST == "1",
  statusline = {
    enabled = statusline_config.enabled ~= false,
    left = statusline_config.left or { "problem_name", "phase", "solve_elapsed" },
    right = statusline_config.right
      or { "reviews_today", "new_today", "new_left", "reviews_total", "due_now",
        "due_later_today", "hint_requested", "outline_revealed", "bookmarked",
        "open_bookmarks", "action" },
    separator = statusline_config.separator or " · ",
  },
})

vim.api.nvim_create_autocmd("FileType", {
  callback = function(event)
    vim.bo[event.buf].completefunc = ""
    vim.bo[event.buf].omnifunc = ""
    vim.bo[event.buf].tagfunc = ""
  end,
  desc = "Disable completion helpers during problem-solving practice",
})

if vim.env.PROBLEM_SOLVING_AUTOSTART ~= "0" then
  vim.api.nvim_create_autocmd("VimEnter", {
    once = true,
    callback = function()
      if vim.env.PROBLEM_SOLVING_SYNC_FIRST == "1" then
        problem_solving.sync_first()
        problem_solving.start()
      else
        vim.schedule(problem_solving.start)
      end
    end,
    desc = "Start problem-solving practice",
  })
end
