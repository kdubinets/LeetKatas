local session = require("problem_solving.session")
local sync = require("problem_solving.sync")
local log = require("practice.log")

local M = {}
local options = nil
local ratings = { "again", "hard", "good", "easy" }

local function map(lhs, rhs, description)
  vim.keymap.set("n", lhs, rhs, { silent = true, desc = description })
end

function M.setup(config)
  options = config
  log.setup(config.log_path)
  session.setup(config)
  sync.setup(config)

  vim.api.nvim_create_autocmd({ "FocusLost", "VimSuspend" }, {
    callback = session.focus_lost, desc = "Pause problem-solving timing",
  })
  vim.api.nvim_create_autocmd({ "FocusGained", "VimResume" }, {
    callback = session.focus_gained, desc = "Resume problem-solving timing",
  })
  vim.api.nvim_create_autocmd("VimLeavePre", {
    callback = function()
      log.event("problem_solving_session_ended", "info", { state = session.get_state().status })
    end,
    desc = "Finish the problem-solving diagnostic session",
  })

  vim.api.nvim_create_user_command("ProblemSolvingStart", function(command)
    session.start(command.args ~= "" and command.args or nil)
  end, { nargs = "?", complete = "dir", desc = "Start problem-solving practice" })
  vim.api.nvim_create_user_command("ProblemSolvingHint", session.hint,
    { desc = "Reveal the optional hint" })
  vim.api.nvim_create_user_command("ProblemSolvingReveal", function(command)
    session.reveal(command.bang)
  end, { bang = true, desc = "Reveal the solution outline; use ! when giving up" })
  vim.api.nvim_create_user_command("ProblemSolvingBookmark", function(command)
    session.bookmark(command.args ~= "" and command.args or nil)
  end, { nargs = "?", desc = "Bookmark the active problem" })
  vim.api.nvim_create_user_command("ProblemSolvingBookmarks", session.bookmarks,
    { desc = "List open-thinking bookmarks" })
  vim.api.nvim_create_user_command("ProblemSolvingReopen", function(command)
    session.reopen(command.args)
  end, { nargs = 1, desc = "Reopen a bookmarked problem" })
  vim.api.nvim_create_user_command("ProblemSolvingUnbookmark", session.unbookmark,
    { desc = "Remove the active bookmark" })
  vim.api.nvim_create_user_command("ProblemSolvingNote", function(command)
    session.note(command.args ~= "" and command.args or nil)
  end, { nargs = "?", desc = "Add a private bookmark note" })
  vim.api.nvim_create_user_command("ProblemSolvingAsk", function(command)
    session.ask(command.args ~= "" and command.args or nil)
  end, { nargs = "?", desc = "Clarify the brief or discuss the revealed solution" })
  vim.api.nvim_create_user_command("ProblemSolvingRate", function(command)
    session.rate(command.args)
  end, {
    nargs = 1,
    complete = function(lead)
      return vim.tbl_filter(function(value) return vim.startswith(value, lead:lower()) end, ratings)
    end,
    desc = "Rate the revealed problem",
  })
  vim.api.nvim_create_user_command("ProblemSolvingNext", session.next,
    { desc = "Open the next problem" })
  vim.api.nvim_create_user_command("ProblemSolvingQuit", session.quit,
    { desc = "End problem-solving practice" })
  vim.api.nvim_create_user_command("ProblemSolvingStats", function(command)
    session.stats(command.args ~= "" and command.args or nil)
  end, { nargs = "?", complete = "dir", desc = "Show problem-solving statistics" })
  vim.api.nvim_create_user_command("ProblemSolvingSync", function()
    sync.manual(session.get_state().collection or options.default_directory)
  end, { desc = "Synchronize problem-solving history" })
  vim.api.nvim_create_user_command("ProblemSolvingLog", log.open,
    { desc = "Open the problem-solving diagnostic log" })
  vim.api.nvim_create_user_command("ProblemSolvingDiagnostics", function()
    local state = session.get_state()
    sync.diagnostics(state.collection or options.default_directory, function(sync_state)
      local pending = sync_state.pending or {}
      vim.notify("Log: " .. log.path() .. "\nState: " .. state.status
        .. "\nSync: " .. tostring(sync_state.status)
        .. "\nPending: " .. tostring((pending.reviews or 0)
          + (pending.bookmarks or 0) + (pending.artifacts or 0)),
        vim.log.levels.INFO, { title = "Problem Solving Diagnostics" })
    end)
  end, { desc = "Show problem-solving diagnostics" })

  map("<leader>ps", M.start, "Problem solving: start")
  map("<leader>ph", M.hint, "Problem solving: hint")
  map("<leader>pr", M.reveal, "Problem solving: reveal outline")
  map("<leader>pg", function() session.reveal(true) end, "Problem solving: give up and reveal")
  map("<leader>pb", M.bookmark, "Problem solving: bookmark")
  map("<leader>pl", M.bookmarks, "Problem solving: list bookmarks")
  map("<leader>pm", M.note, "Problem solving: private note")
  map("<leader>pc", M.ask, "Problem solving: conversation")
  map("<leader>p1", function() M.rate("again") end, "Problem solving: rate Again")
  map("<leader>p2", function() M.rate("hard") end, "Problem solving: rate Hard")
  map("<leader>p3", function() M.rate("good") end, "Problem solving: rate Good")
  map("<leader>p4", function() M.rate("easy") end, "Problem solving: rate Easy")
  map("<leader>pn", M.next, "Problem solving: next")
  map("<leader>pt", M.stats, "Problem solving: statistics")
  map("<leader>pq", M.quit, "Problem solving: quit")
end

function M.start(directory) return session.start(directory) end
function M.hint() return session.hint() end
function M.reveal() return session.reveal(false) end
function M.bookmark(note) return session.bookmark(note) end
function M.bookmarks() return session.bookmarks() end
function M.reopen(problem_id) return session.reopen(problem_id) end
function M.unbookmark() return session.unbookmark() end
function M.note(note) return session.note(note) end
function M.ask(question) return session.ask(question) end
function M.rate(rating) return session.rate(rating) end
function M.begin_discussion() return session.begin_discussion() end
function M.next() return session.next() end
function M.quit() return session.quit() end
function M.stats(directory) return session.stats(directory) end
function M.sync_first(directory) return sync.sync_first(directory) end
function M.get_state() return session.get_state() end

return M
