local init_path = debug.getinfo(1, "S").source:sub(2)
local driver_dir = vim.fn.fnamemodify(init_path, ":p:h")
local repository_dir = vim.fn.fnamemodify(driver_dir, ":h:h")

vim.g.mapleader = " "
vim.g.maplocalleader = " "

vim.opt.loadplugins = false
vim.opt.swapfile = false
vim.opt.termguicolors = true
pcall(function()
  vim.opt.autocomplete = false
end)

vim.cmd("filetype on")
vim.cmd("syntax enable")

package.path = table.concat({
  driver_dir .. "/lua/?.lua",
  driver_dir .. "/lua/?/init.lua",
  package.path,
}, ";")

local selected_python = vim.env.PRACTICE_PYTHON
  or (vim.fn.executable(repository_dir .. "/.venv/bin/python") == 1
    and repository_dir .. "/.venv/bin/python" or "python3")

local function load_user_config()
  -- An empty Lua table is encoded as JSON [], so mark this one as an object.
  local request = vim.empty_dict()
  if vim.env.PRACTICE_CONFIG and vim.env.PRACTICE_CONFIG ~= "" then
    request.path = vim.env.PRACTICE_CONFIG
  end
  local output = vim.fn.system(
    { selected_python, repository_dir .. "/src/scripts/load_practice_config.py" },
    vim.json.encode(request)
  )
  local ok, response = pcall(vim.json.decode, output)
  if vim.v.shell_error ~= 0 or not ok or type(response) ~= "table" or response.error then
    local detail = ok and type(response) == "table" and response.error or output
    error("Invalid practice configuration: " .. tostring(detail))
  end
  return response.config or {}
end

local user_config = load_user_config()
local practice_config = user_config.practice or {}
local reviewer_config = user_config.reviewer or {}
local editor_config = user_config.editor or {}
local evaluation_config = user_config.evaluation or {}
local sync_config = user_config.sync or {}
local statusline_config = user_config.statusline or {}

local function environment(name)
  local value = vim.env[name]
  return value ~= nil and value ~= "" and value or nil
end

local review_archive_ttl_days = tonumber(environment("PRACTICE_REVIEW_ARCHIVE_TTL_DAYS")
  or practice_config.review_archive_ttl_days or 30)
if not review_archive_ttl_days or review_archive_ttl_days % 1 ~= 0
  or review_archive_ttl_days < 0 or review_archive_ttl_days > 3650
then
  error("PRACTICE_REVIEW_ARCHIVE_TTL_DAYS must be an integer between 0 and 3650")
end

local indent_width = editor_config.indent_width or 4
vim.opt.expandtab = true
vim.opt.shiftwidth = indent_width
vim.opt.softtabstop = indent_width
vim.opt.tabstop = indent_width

local function setup_which_key(delay)
  local plugin_dir = vim.fn.stdpath("data") .. "/leetkatas/which-key.nvim"
  if vim.fn.isdirectory(plugin_dir) == 0 and vim.env.PRACTICE_INSTALL_PLUGINS == "1" then
    local install = vim.fn.confirm(
      "Practice can download and run which-key.nvim v3.17.0 from GitHub. Install it?",
      "&Install\n&Skip",
      2
    )
    if install ~= 1 then
      return
    end
    vim.fn.mkdir(vim.fn.fnamemodify(plugin_dir, ":h"), "p")
    local output = vim.fn.system({
      "git", "clone", "--filter=blob:none", "--branch=v3.17.0", "--single-branch",
      "https://github.com/folke/which-key.nvim.git", plugin_dir,
    })
    if vim.v.shell_error ~= 0 then
      vim.schedule(function()
        vim.notify("Could not install which-key.nvim:\n" .. output, vim.log.levels.WARN,
          { title = "Practice" })
      end)
      return
    end
  end
  if vim.fn.isdirectory(plugin_dir) == 0 then
    return
  end

  vim.opt.runtimepath:prepend(plugin_dir)
  local ok, which_key = pcall(require, "which-key")
  if ok then
    which_key.setup({ delay = delay })
  else
    vim.schedule(function()
      vim.notify("The cached which-key.nvim plugin could not be loaded.", vim.log.levels.WARN,
        { title = "Practice" })
    end)
  end
end

setup_which_key(editor_config.which_key_delay_ms or 300)

local practice = require("practice")
local function reviewer_provider(value, setting)
  if value == "codex" or value == "openai" then return value end
  error(setting .. " must be codex or openai")
end
local reviewer_provider_name = reviewer_provider(
  environment("PRACTICE_REVIEWER_PROVIDER") or reviewer_config.provider or "codex",
  "PRACTICE_REVIEWER_PROVIDER"
)
local follow_up_provider_name = reviewer_provider(
  environment("PRACTICE_FOLLOW_UP_REVIEWER_PROVIDER") or reviewer_config.follow_up_provider
    or reviewer_provider_name,
  "PRACTICE_FOLLOW_UP_REVIEWER_PROVIDER"
)
local reviewer_model = environment("PRACTICE_REVIEW_MODEL") or reviewer_config.model or "gpt-5.6-luna"
local reviewer_reasoning_effort = environment("PRACTICE_REVIEW_EFFORT")
  or reviewer_config.reasoning_effort or "low"
local follow_up_model = environment("PRACTICE_FOLLOW_UP_MODEL")
  or reviewer_config.follow_up_model or reviewer_model
local follow_up_reasoning_effort = environment("PRACTICE_FOLLOW_UP_EFFORT")
  or reviewer_config.follow_up_reasoning_effort or reviewer_reasoning_effort
local default_reviewer_command = {
  selected_python,
  repository_dir .. "/src/scripts/"
    .. (reviewer_provider_name == "openai" and "openai_reviewer.py" or "codex_reviewer.py"),
  "--model",
  reviewer_model,
  "--effort",
  reviewer_reasoning_effort,
}
local default_follow_up_command = {
  selected_python,
  repository_dir .. "/src/scripts/"
    .. (follow_up_provider_name == "openai" and "openai_reviewer.py" or "codex_reviewer.py"),
  "--follow-up",
  "--model",
  follow_up_model,
  "--effort",
  follow_up_reasoning_effort,
}
local compiler = environment("CXX") or evaluation_config.compiler
if not compiler then
  compiler = environment("PRACTICE_COMPILER") == "gcc" and "g++" or "clang++"
end

practice.setup({
  python = selected_python,
  log_path = environment("PRACTICE_LOG") or practice_config.log_path
    or (vim.fn.stdpath("state") .. "/leetkatas/practice.log"),
  scripts_dir = repository_dir .. "/src/scripts",
  database_path = environment("PRACTICE_DATABASE") or practice_config.database_path,
  supabase_url = environment("PRACTICE_SUPABASE_URL") or sync_config.supabase_url,
  sync_first = vim.env.PRACTICE_SYNC_FIRST == "1",
  review_archive_ttl_days = review_archive_ttl_days,
  notes_directory = environment("PRACTICE_NOTES_DIRECTORY") or practice_config.notes_directory
    or ((environment("XDG_DATA_HOME") or vim.fn.expand("~/.local/share"))
      .. "/leetkatas/notes"),
  default_directory = environment("PRACTICE_COLLECTION") or practice_config.collection
    or (practice_config.collections and practice_config.collections[1])
    or repository_dir .. "/practice/cpp/collections/core",
  default_directories = environment("PRACTICE_COLLECTION") and { environment("PRACTICE_COLLECTION") }
    or practice_config.collections
    or { practice_config.collection or repository_dir .. "/practice/cpp/collections/core" },
  source_extension = environment("PRACTICE_SOURCE_EXTENSION") or ".cpp",
  metadata_extension = environment("PRACTICE_METADATA_EXTENSION") or ".md",
  practice_marker = environment("PRACTICE_MARKER") or "// Finish:",
  enhanced_syntax_highlighting = editor_config.enhanced_syntax_highlighting ~= false,
  local_completion = editor_config.local_completion == true,
  statusline = {
    enabled = statusline_config.enabled ~= false,
    left = statusline_config.left or { "exercise_name" },
    right = statusline_config.right
      or { "solve_elapsed", "time_today", "reviews_today", "due_now", "new_left" },
    separator = statusline_config.separator or " · ",
  },
  evaluation_command = {
    compiler,
    "-std=c++20",
    "-Wall",
    "-Wextra",
    "-fsyntax-only",
    "{source}",
  },
  reviewer = environment("PRACTICE_REVIEWER") and {
    command = { environment("PRACTICE_REVIEWER") }, name = environment("PRACTICE_REVIEWER_NAME")
  } or {
    command = default_reviewer_command,
    name = reviewer_provider_name == "openai" and "OpenAI API" or "Codex",
    model = reviewer_model,
    reasoning_effort = reviewer_reasoning_effort,
  },
  follow_up_reviewer = (environment("PRACTICE_FOLLOW_UP_REVIEWER")
      or environment("PRACTICE_REVIEWER")) and {
    command = { environment("PRACTICE_FOLLOW_UP_REVIEWER")
      or environment("PRACTICE_REVIEWER") },
    name = environment("PRACTICE_FOLLOW_UP_REVIEWER_NAME")
      or environment("PRACTICE_REVIEWER_NAME"),
    model = follow_up_model,
    reasoning_effort = follow_up_reasoning_effort,
  } or {
    command = default_follow_up_command,
    name = follow_up_provider_name == "openai" and "OpenAI API" or "Codex",
    model = follow_up_model,
    reasoning_effort = follow_up_reasoning_effort,
  },
})

vim.api.nvim_create_autocmd("FileType", {
  callback = function(event)
    vim.bo[event.buf].completefunc = ""
    vim.bo[event.buf].omnifunc = ""
    vim.bo[event.buf].tagfunc = ""
  end,
  desc = "Disable completion helpers during practice",
})

if vim.env.PRACTICE_AUTOSTART ~= "0" then
  vim.api.nvim_create_autocmd("VimEnter", {
    once = true,
    callback = function()
      if vim.env.PRACTICE_SYNC_FIRST == "1" then
        practice.sync_first()
        practice.start()
        return
      end
      vim.schedule(function()
        practice.start()
      end)
    end,
    desc = "Start the coding practice session",
  })
end
