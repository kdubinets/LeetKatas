local session = require("practice.session")
local log = require("practice.log")
local sync = require("practice.sync")
local statusline = require("practice.statusline")

local M = {}

local RATINGS = { "fail", "acceptable", "good", "excellent" }
local NOTE_KINDS = { "follow-up", "research", "exercise-fix" }
local PRACTICE_KEYS = {
  "<leader>s", "<leader>b", "<leader>c", "<leader>a", "<leader>R", "<leader>r", "<leader>1",
  "<leader>2", "<leader>3", "<leader>4", "<leader>n", "<leader>m", "<leader>d", "<leader>D",
  "<leader>f", "<leader>i", "<leader>o", "<leader>t", "<leader>q",
}

local function map(lhs, rhs, description)
  vim.keymap.set("n", lhs, rhs, { silent = true, desc = description })
end

local function clear_practice_maps(mode)
  for _, lhs in ipairs(PRACTICE_KEYS) do
    pcall(vim.keymap.del, mode, lhs)
  end
end

function M.refresh_keymaps()
  clear_practice_maps("n")
  clear_practice_maps("x")

  local status = session.get_state().status
  map("<leader>o", M.open_notes, "Notes")
  map("<leader>t", M.stats, "Statistics")

  if status == "idle" or status == "complete" then
    map("<leader>s", M.start, "Start practice")
    return
  end

  if status == "solving" then
    map("<leader>b", M.compile, "Compile only")
    map("<leader>c", M.submit, "Check solution")
    map("<leader>n", M.next, "Skip exercise")
    map("<leader>d", M.disable, "Disable exercise")
    map("<leader>D", M.delete, "Delete exercise")
    map("<leader>m", M.note, "Add note")
    vim.keymap.set("x", "<leader>m", ":PracticeNote<CR>", {
      silent = true, desc = "Add note",
    })
    map("<leader>i", M.fold_imports, "Toggle imports")
    map("<leader>q", M.quit, "End practice")
    return
  end

  if status == "post_rating" then
    map("<leader>b", M.compile, "Compile only")
    map("<leader>n", M.next, "Next exercise")
    map("<leader>d", M.disable, "Disable exercise")
    map("<leader>D", M.delete, "Delete exercise")
    map("<leader>m", M.note, "Add note")
    map("<leader>i", M.fold_imports, "Toggle imports")
    map("<leader>q", M.quit, "End practice")
    return
  end

  if status == "reviewing" then
    map("<leader>a", M.accept, "Accept rating")
    map("<leader>R", M.accept_stay, "Accept rating and keep editing")
    map("<leader>1", function() M.rate("fail") end, "Rate: Fail")
    map("<leader>2", function() M.rate("acceptable") end, "Rate: Acceptable")
    map("<leader>3", function() M.rate("good") end, "Rate: Good")
    map("<leader>4", function() M.rate("excellent") end, "Rate: Excellent")
    map("<leader>r", M.retry, "Retry exercise")
    map("<leader>n", M.next, "Skip exercise")
    map("<leader>d", M.disable, "Disable exercise")
    map("<leader>D", M.delete, "Delete exercise")
    map("<leader>m", M.note, "Add note")
    vim.keymap.set("x", "<leader>m", ":PracticeNote<CR>", {
      silent = true, desc = "Add note",
    })
    map("<leader>f", M.ask, "Ask reviewer")
    map("<leader>q", M.quit, "End practice")
  end
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
  options.on_status_change = M.refresh_keymaps
  session.setup(options)
  sync.setup(options)

  vim.api.nvim_create_user_command("PracticeStart", function(command)
    session.start(command.args ~= "" and command.args or nil)
  end, { nargs = "?", complete = "dir", desc = "Start a coding practice session" })

  vim.api.nvim_create_user_command("PracticeSubmit", session.submit, {
    desc = "Submit the current practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeCompile", session.compile, {
    desc = "Compile without submitting for review",
  })
  vim.api.nvim_create_user_command("PracticeAccept", session.accept, {
    desc = "Accept the proposed practice rating",
  })
  vim.api.nvim_create_user_command("PracticeAcceptStay", session.accept_stay, {
    desc = "Accept the proposed rating and keep editing",
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
  vim.api.nvim_create_user_command("PracticeRateStay", function(command)
    session.rate(command.args, true)
  end, { nargs = 1, complete = function(argument_lead)
    return vim.tbl_filter(function(rating) return vim.startswith(rating, argument_lead:lower()) end, RATINGS)
  end, desc = "Record a rating and keep editing" })
  vim.api.nvim_create_user_command("PracticeNext", session.next, {
    desc = "Skip to the next practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeDisable", session.disable, {
    desc = "Disable the current exercise from future selection",
  })
  vim.api.nvim_create_user_command("PracticeDelete", session.delete, {
    desc = "Permanently delete the current exercise from its collection",
  })
  vim.api.nvim_create_user_command("PracticeEnable", function(command)
    session.enable(nil, command.args)
  end, { nargs = 1, desc = "Re-enable a disabled exercise by ID" })
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

  M.refresh_keymaps()
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

function M.compile()
  session.compile()
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

function M.accept_stay()
  session.accept_stay()
end

function M.next()
  session.next()
end

function M.disable()
  session.disable()
end

function M.delete()
  session.delete()
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
