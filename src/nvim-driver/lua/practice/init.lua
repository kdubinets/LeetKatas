local session = require("practice.session")
local log = require("practice.log")
local sync = require("practice.sync")
local statusline = require("practice.statusline")

local M = {}

local RATINGS = { "fail", "acceptable", "good", "excellent" }
local NOTE_KINDS = { "follow-up", "research", "exercise-fix" }

local function map(lhs, rhs, description)
  vim.keymap.set("n", lhs, rhs, { silent = true, desc = description })
end

function M.setup(options)
  log.setup(options.log_path)
  vim.api.nvim_create_autocmd("VimLeavePre", {
    callback = function()
      statusline.stop()
      log.event("session_ended", "info", { state = session.get_state().status })
    end,
    desc = "Finish the practice diagnostic session",
  })
  vim.api.nvim_create_autocmd({ "FocusLost", "VimSuspend" }, {
    callback = session.focus_lost,
    desc = "Pause active practice timing",
  })
  vim.api.nvim_create_autocmd({ "FocusGained", "VimResume" }, {
    callback = session.focus_gained,
    desc = "Resume active practice timing",
  })
  session.setup(options)
  sync.setup(options)

  vim.api.nvim_create_user_command("PracticeStart", function(command)
    session.start(command.args ~= "" and command.args or nil)
  end, { nargs = "?", complete = "dir", desc = "Start a coding practice session" })

  vim.api.nvim_create_user_command("PracticeSubmit", session.submit, {
    desc = "Submit the current practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeAccept", session.accept, {
    desc = "Accept the proposed practice rating",
  })
  vim.api.nvim_create_user_command("PracticeAsk", function(command)
    session.ask(command.args ~= "" and command.args or nil)
  end, {
    nargs = "*",
    desc = "Ask the reviewer a follow-up question",
  })
  vim.api.nvim_create_user_command("PracticeRetry", session.retry, {
    desc = "Return to the current source without recording a rating",
  })
  vim.api.nvim_create_user_command("PracticeRate", function(command)
    session.rate(command.args)
  end, {
    nargs = 1,
    complete = function(argument_lead)
      return vim.tbl_filter(function(rating)
        return vim.startswith(rating, argument_lead:lower())
      end, RATINGS)
    end,
    desc = "Override the proposed practice rating",
  })
  vim.api.nvim_create_user_command("PracticeNext", session.next, {
    desc = "Skip to the next practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeQuit", session.quit, {
    desc = "End the coding practice session",
  })
  vim.api.nvim_create_user_command("PracticeNote", function(command)
    session.note(command.args ~= "" and command.args or nil,
      command.range > 0 and command.line1 or nil,
      command.range > 0 and command.line2 or nil)
  end, {
    nargs = "?",
    range = true,
    complete = function(argument_lead)
      return vim.tbl_filter(function(kind)
        return vim.startswith(kind, argument_lead:lower())
      end, NOTE_KINDS)
    end,
    desc = "Capture a note for the active practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeNotes", session.open_notes, {
    desc = "Open the practice notes directory",
  })
  vim.api.nvim_create_user_command("PracticeStats", function(command)
    session.stats(command.args ~= "" and command.args or nil)
  end, {
    nargs = "?",
    complete = "dir",
    desc = "Show practice statistics for a collection",
  })
  vim.api.nvim_create_user_command("PracticeSync", function()
    local state = session.get_state()
    sync.manual(state.collections or options.default_directories)
  end, { desc = "Synchronize practice review history" })
  vim.api.nvim_create_user_command("PracticeLog", log.open, {
    desc = "Open the persistent practice diagnostic log",
  })
  vim.api.nvim_create_user_command("PracticeDiagnostics", function()
    local state = session.get_state()
    log.event("diagnostics_requested", "info", {
      state = state.status,
      exercise_id = state.exercise and state.exercise.id or nil,
    })
    sync.diagnostics(state.collections or options.default_directories, function(sync_state)
      local successful = sync_state.last_success or "never"
      vim.notify("Practice log: " .. log.path() .. "\nSession: " .. log.session_id()
        .. "\nState: " .. state.status
        .. "\nSync configured: " .. tostring(sync_state.configured == true)
        .. "\nLast successful sync: " .. successful
        .. "\nPending uploads: " .. tostring(sync_state.pending or 0),
        vim.log.levels.INFO, { title = "Practice Diagnostics" })
    end)
  end, { desc = "Show practice diagnostic location and session state" })

  map("<leader>s", M.start, "Practice: start")
  map("<leader>c", M.submit, "Practice: check current solution")
  map("<leader>a", M.accept, "Practice: after review, accept proposed rating")
  map("<leader>r", M.retry, "Practice: retry current exercise without recording")
  map("<leader>1", function() M.rate("fail") end, "Practice: after review, rate Fail")
  map("<leader>2", function() M.rate("acceptable") end, "Practice: after review, rate Acceptable")
  map("<leader>3", function() M.rate("good") end, "Practice: after review, rate Good")
  map("<leader>4", function() M.rate("excellent") end, "Practice: after review, rate Excellent")
  map("<leader>n", M.next, "Practice: next exercise")
  map("<leader>m", M.note, "Practice: capture a follow-up note")
  map("<leader>f", M.ask, "Practice: ask reviewer a follow-up question")
  map("<leader>i", M.fold_imports, "Practice: toggle imports")
  vim.keymap.set("x", "<leader>m", ":PracticeNote<CR>", {
    silent = true, desc = "Practice: capture selected context in a follow-up note",
  })
  map("<leader>o", M.open_notes, "Practice: open notes directory")
  map("<leader>t", M.stats, "Practice: show statistics")
  map("<leader>q", M.quit, "Practice: quit")
end

function M.start(directory)
  session.start(directory)
end

function M.sync_first(directory)
  return sync.sync_first(directory)
end

function M.submit()
  session.submit()
end

function M.accept()
  session.accept()
end

function M.rate(rating)
  session.rate(rating)
end

function M.retry()
  session.retry()
end

function M.next()
  session.next()
end

function M.quit()
  session.quit()
end

function M.note(kind, first_line, last_line)
  return session.note(kind, first_line, last_line)
end

function M.ask(question)
  return session.ask(question)
end

function M.open_notes()
  session.open_notes()
end

function M.fold_imports()
  session.fold_imports()
end

function M.stats(directory)
  session.stats(directory)
end

function M.get_state()
  return session.get_state()
end

return M
