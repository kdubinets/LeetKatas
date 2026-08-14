local session = require("problem_solving.session")
local sync = require("problem_solving.sync")
local log = require("practice.log")
local statusline = require("problem_solving.statusline")
local implementation = require("problem_solving.implementation_session")

local M = {}
local options = nil
local ratings = { "again", "hard", "good", "easy" }
local PROBLEM_SOLVING_KEYS = {
  "<leader>s", "<leader>h", "<leader>i", "<leader>d", "<leader>r",
  "<leader>b", "<leader>l", "<leader>m", "<leader>c", "<leader>1",
  "<leader>2", "<leader>3", "<leader>4", "<leader>n", "<leader>t",
  "<leader>q",
}

local function map(lhs, rhs, description)
  vim.keymap.set("n", lhs, rhs, { silent = true, desc = description })
end

local function clear_maps()
  for _, lhs in ipairs(PROBLEM_SOLVING_KEYS) do
    pcall(vim.keymap.del, "n", lhs)
  end
end

function M.refresh_keymaps()
  clear_maps()
  if implementation.active() then return end

  local status = session.get_state().status
  map("<leader>t", M.stats, "Statistics")
  map("<leader>d", function()
    implementation.drafts(session.get_state().collection or options.default_directory)
  end, "Implementation drafts")

  if status == "idle" or status == "complete" then
    map("<leader>s", M.start, "Start practice")
    return
  end

  if status == "solving" then
    map("<leader>h", M.hint, "Show hint")
    map("<leader>r", M.reveal, "Reveal outline")
  end

  if status == "solving" or status == "revealed" or status == "discussing" then
    map("<leader>i", implementation.open_active, "Implement")
    map("<leader>b", M.bookmark, "Bookmark")
    map("<leader>l", M.bookmarks, "Bookmarks")
    map("<leader>m", M.note, "Add note")
    map("<leader>c", M.ask, "Ask reviewer")
    map("<leader>n", M.next, "Next problem")
    map("<leader>q", M.quit, "End practice")
  end

  if status == "revealed" or status == "discussing" then
    map("<leader>1", function() M.rate("again") end, "Rate: Again")
    map("<leader>2", function() M.rate("hard") end, "Rate: Hard")
    map("<leader>3", function() M.rate("good") end, "Rate: Good")
    map("<leader>4", function() M.rate("easy") end, "Rate: Easy")
  end
end

function M.setup(config)
  options = config
  config.on_status_change = M.refresh_keymaps
  config.on_implementation_state_change = M.refresh_keymaps
  log.setup(config.log_path)
  session.setup(config)
  implementation.setup(config, session)
  sync.setup(config)
  statusline.setup(config, session.get_state)

  vim.api.nvim_create_autocmd({ "FocusLost", "VimSuspend" }, {
    callback = session.focus_lost, desc = "Pause problem-solving timing",
  })
  vim.api.nvim_create_autocmd({ "FocusGained", "VimResume" }, {
    callback = session.focus_gained, desc = "Resume problem-solving timing",
  })
  vim.api.nvim_create_autocmd("VimLeavePre", {
    callback = function()
      implementation.shutdown()
      statusline.stop()
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
    session.reveal()
  end, { desc = "Reveal the solution outline" })
  vim.api.nvim_create_user_command("ProblemSolvingImplement", implementation.open_active,
    { desc = "Start or resume Level C implementation" })
  vim.api.nvim_create_user_command("ProblemSolvingDrafts", function(command)
    implementation.drafts(command.args ~= "" and command.args or session.get_state().collection or config.default_directory)
  end, { nargs = "?", complete = "dir", desc = "List current implementation drafts" })
  vim.api.nvim_create_user_command("ProblemSolvingCompile", implementation.compile,
    { desc = "Compile the current implementation draft" })
  vim.api.nvim_create_user_command("ProblemSolvingImplementationCheck", implementation.check,
    { desc = "Request a bounded implementation check" })
  vim.api.nvim_create_user_command("ProblemSolvingFinishImplementation", implementation.finish,
    { desc = "Finish with an implementation review" })
  vim.api.nvim_create_user_command("ProblemSolvingReturn", implementation.return_to_card,
    { desc = "Return to the Level C card" })
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

  M.refresh_keymaps()
end

function M.start(directory) return session.start(directory) end
function M.hint() return session.hint() end
function M.reveal() return session.reveal() end
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
