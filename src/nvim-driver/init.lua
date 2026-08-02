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

local practice = require("practice")
local selected_python = vim.env.PRACTICE_PYTHON
  or (vim.fn.executable(repository_dir .. "/.venv/bin/python") == 1
    and repository_dir .. "/.venv/bin/python" or "python3")

practice.setup({
  python = selected_python,
  log_path = vim.env.PRACTICE_LOG
    or (vim.fn.stdpath("state") .. "/leetkatas/practice.log"),
  scripts_dir = repository_dir .. "/src/scripts",
  database_path = vim.env.PRACTICE_DATABASE,
  default_directory = vim.env.PRACTICE_COLLECTION
    or repository_dir .. "/practice/cpp/collections/core",
  source_extension = vim.env.PRACTICE_SOURCE_EXTENSION or ".cpp",
  metadata_extension = vim.env.PRACTICE_METADATA_EXTENSION or ".md",
  practice_marker = vim.env.PRACTICE_MARKER or "// Finish:",
  evaluation_command = {
    vim.env.CXX or (vim.env.PRACTICE_COMPILER == "gcc" and "g++" or "clang++"),
    "-std=c++20",
    "-Wall",
    "-Wextra",
    "-fsyntax-only",
    "{source}",
  },
  reviewer = vim.env.PRACTICE_REVIEWER and { command = { vim.env.PRACTICE_REVIEWER }, name = vim.env.PRACTICE_REVIEWER_NAME } or {
    command = { selected_python, repository_dir .. "/src/scripts/codex_reviewer.py" }, name = "Codex"
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
