local init_path = debug.getinfo(1, "S").source:sub(2)
local driver_dir = vim.fn.fnamemodify(init_path, ":p:h")
local repository_dir = vim.fn.fnamemodify(driver_dir, ":h:h")

vim.g.mapleader = " "
vim.g.maplocalleader = " "

vim.opt.loadplugins = false
vim.opt.swapfile = false
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

local function environment(name)
  local value = vim.env[name]
  return value ~= nil and value ~= "" and value or nil
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
    which_key.add({ { "<leader>p", group = "practice" } })
  else
    vim.schedule(function()
      vim.notify("The cached which-key.nvim plugin could not be loaded.", vim.log.levels.WARN,
        { title = "Practice" })
    end)
  end
end

setup_which_key(editor_config.which_key_delay_ms or 300)

local practice = require("practice")
local default_reviewer_command = {
  selected_python,
  repository_dir .. "/src/scripts/codex_reviewer.py",
  "--model",
  environment("PRACTICE_REVIEW_MODEL") or reviewer_config.model or "gpt-5.6-luna",
  "--effort",
  environment("PRACTICE_REVIEW_EFFORT") or reviewer_config.reasoning_effort or "low",
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
  default_directory = environment("PRACTICE_COLLECTION") or practice_config.collection
    or repository_dir .. "/practice/cpp/collections/core",
  source_extension = environment("PRACTICE_SOURCE_EXTENSION") or ".cpp",
  metadata_extension = environment("PRACTICE_METADATA_EXTENSION") or ".md",
  practice_marker = environment("PRACTICE_MARKER") or "// Finish:",
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
    command = default_reviewer_command, name = "Codex"
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
      vim.schedule(function()
        practice.start()
      end)
    end,
    desc = "Start the coding practice session",
  })
end
