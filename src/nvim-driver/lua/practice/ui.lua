local M = {}
local log = require("practice.log")

local feedback_buffer = nil
local feedback_window = nil

local function valid_buffer(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
end

local function valid_window(window)
  return window ~= nil and vim.api.nvim_win_is_valid(window)
end

local function append_text(lines, text)
  local text_lines = vim.split(text or "", "\n", { plain = true })
  vim.list_extend(lines, text_lines)
end

local function set_feedback_lines(lines)
  if not valid_buffer(feedback_buffer) then
    return
  end
  vim.bo[feedback_buffer].modifiable = true
  vim.bo[feedback_buffer].readonly = false
  vim.api.nvim_buf_set_lines(feedback_buffer, 0, -1, false, lines)
  vim.bo[feedback_buffer].filetype = "markdown"
  vim.bo[feedback_buffer].buftype = "nofile"
  vim.bo[feedback_buffer].bufhidden = "wipe"
  vim.bo[feedback_buffer].swapfile = false
  vim.bo[feedback_buffer].modifiable = false
  vim.bo[feedback_buffer].readonly = true
end

local function ensure_feedback(source_window, focus_feedback)
  if valid_window(feedback_window) and valid_buffer(feedback_buffer) then
    if focus_feedback then
      vim.api.nvim_set_current_win(feedback_window)
    end
    return
  end
  M.close_feedback()
  if valid_window(source_window) then
    vim.api.nvim_set_current_win(source_window)
  end
  if vim.o.columns < 120 then
    vim.cmd("botright split")
  else
    vim.cmd("botright vsplit")
  end
  feedback_window = vim.api.nvim_get_current_win()
  feedback_buffer = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(feedback_window, feedback_buffer)
  if vim.o.columns < 120 then
    vim.api.nvim_win_set_height(feedback_window, math.max(10, math.floor(vim.o.lines / 3)))
  else
    vim.api.nvim_win_set_width(feedback_window, math.max(40, math.floor(vim.o.columns / 3)))
  end
  vim.wo[feedback_window].number = false
  vim.wo[feedback_window].relativenumber = false
  vim.wo[feedback_window].signcolumn = "no"
  vim.wo[feedback_window].wrap = true
  if not focus_feedback and valid_window(source_window) then
    vim.api.nvim_set_current_win(source_window)
  end
end

function M.notify(message, level)
  log.event("notification", level == vim.log.levels.ERROR and "error" or "info", {
    message = message,
    nvim_level = level,
  })
  vim.notify(message, level or vim.log.levels.INFO, { title = "Practice" })
end

function M.confirm_discard(action)
  local choice = vim.fn.confirm(
    "The current attempt has unsaved changes. Discard them and " .. action .. "?",
    "&Discard\n&Cancel",
    2
  )
  return choice == 1
end

function M.close_feedback()
  if valid_window(feedback_window) then
    vim.api.nvim_win_close(feedback_window, true)
  end
  if valid_buffer(feedback_buffer) then
    vim.api.nvim_buf_delete(feedback_buffer, { force = true })
  end
  feedback_window = nil
  feedback_buffer = nil
end

function M.open_source(path, preferred_window, practice_marker)
  M.close_feedback()
  if valid_window(preferred_window) then
    vim.api.nvim_set_current_win(preferred_window)
  end

  vim.cmd("edit! " .. vim.fn.fnameescape(path))
  local buffer = vim.api.nvim_get_current_buf()
  local window = vim.api.nvim_get_current_win()
  vim.bo[buffer].bufhidden = "wipe"
  vim.bo[buffer].swapfile = false
  vim.bo[buffer].completefunc = ""
  vim.bo[buffer].omnifunc = ""
  vim.bo[buffer].tagfunc = ""

  local lines = vim.api.nvim_buf_get_lines(buffer, 0, -1, false)
  for index, line in ipairs(lines) do
    local marker_start = line:find(practice_marker, 1, true)
    if marker_start then
      vim.api.nvim_win_set_cursor(window, { index, marker_start - 1 })
      break
    end
  end
  return buffer, window
end

function M.open_feedback(source_window, result)
  ensure_feedback(source_window, true)

  local compilation = result.compiled and "SUCCESS" or "FAILED"
  local proposed = "Unavailable"
  if type(result.proposed_rating) == "string" then
    proposed = result.proposed_rating:sub(1, 1):upper() .. result.proposed_rating:sub(2)
  end
  local lines = {
    "# Practice Feedback",
    "",
    "**Compilation:** " .. compilation,
    "",
    "**Proposed rating:** " .. proposed,
    "",
    "- `<Space>pa` accept " .. proposed,
    "- `<Space>p1` Fail",
    "- `<Space>p2` Acceptable",
    "- `<Space>p3` Good",
    "- `<Space>p4` Excellent",
    "- `<Space>pn` skip without recording",
    "",
    "## Compiler diagnostics",
    "",
    "```text",
  }
  append_text(lines, result.diagnostics ~= "" and result.diagnostics or "(none)")
  vim.list_extend(lines, { "```", "", "## Reviewer", "", "**Status:** " .. tostring(result.review.status), "" })
  if result.review.status == "available" and result.review.feedback then
    local review = result.review.feedback
    append_text(lines, "**Verdict:** " .. review.verdict .. "\n\n" .. review.summary .. "\n\n" .. review.correctness_analysis .. "\n\n**Code quality:** " .. review.code_quality_analysis)
  else
    append_text(lines, "Reviewer unavailable: " .. tostring(result.review.failure) .. "\n\nChoose a manual rating below.")
  end
  vim.list_extend(lines, { "", "---", "" })
  append_text(lines, result.metadata)

  set_feedback_lines(lines)
  vim.api.nvim_win_set_cursor(feedback_window, { 1, 0 })

  return feedback_buffer, feedback_window
end

function M.open_progress(source_window)
  ensure_feedback(source_window, false)
  M.update_progress(0, {})
  return feedback_buffer, feedback_window
end

function M.update_progress(elapsed_seconds, events)
  if not valid_buffer(feedback_buffer) then
    return
  end
  local frames = { "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏" }
  local frame = frames[(math.floor(elapsed_seconds * 10) % #frames) + 1]
  local compilation = nil
  local attempt = nil
  local maximum_attempts = 3
  local retry_delay = nil
  local review_finished = nil
  for _, event in ipairs(events) do
    if event.event == "compilation_finished" then
      compilation = event.compiled
    elseif event.event == "review_attempt_started" then
      attempt = event.attempt
      maximum_attempts = event.maximum_attempts or maximum_attempts
      retry_delay = nil
    elseif event.event == "review_retry_scheduled" then
      retry_delay = event.delay_seconds
    elseif event.event == "review_finished" then
      review_finished = event.status
    end
  end
  local lines = {
    "# Practice Evaluation",
    "",
    string.format("%s **Working…** %.1fs", frame, elapsed_seconds),
    "",
    "✓ Source saved",
  }
  if compilation == nil then
    table.insert(lines, frame .. " Compiling submission")
  else
    table.insert(lines, (compilation and "✓" or "✗") .. " Compilation "
      .. (compilation and "succeeded" or "failed; continuing to review"))
    if review_finished then
      table.insert(lines, "✓ Reviewer finished: " .. review_finished)
    elseif retry_delay then
      table.insert(lines, string.format("%s Reviewer retry %d of %d in %.1fs", frame,
        (attempt or 0) + 1, maximum_attempts, retry_delay))
    elseif attempt then
      table.insert(lines, string.format("%s LLM review — attempt %d of %d", frame,
        attempt, maximum_attempts))
    else
      table.insert(lines, frame .. " Starting LLM reviewer")
    end
  end
  vim.list_extend(lines, { "", "The final feedback will replace this pane automatically." })
  set_feedback_lines(lines)
end

function M.show_progress_error(error_message)
  set_feedback_lines({
    "# Practice Evaluation Failed",
    "",
    tostring(error_message),
    "",
    "Return to the source, correct the configuration or submission, and check again.",
  })
end

return M
