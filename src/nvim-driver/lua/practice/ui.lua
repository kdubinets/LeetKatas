local M = {}

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

function M.notify(message, level)
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

  local compilation = result.compiled and "SUCCESS" or "FAILED"
  local proposed = result.proposed_rating:sub(1, 1):upper() .. result.proposed_rating:sub(2)
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
  vim.list_extend(lines, { "```", "", "---", "" })
  append_text(lines, result.metadata)

  vim.bo[feedback_buffer].modifiable = true
  vim.api.nvim_buf_set_lines(feedback_buffer, 0, -1, false, lines)
  vim.bo[feedback_buffer].filetype = "markdown"
  vim.bo[feedback_buffer].buftype = "nofile"
  vim.bo[feedback_buffer].bufhidden = "wipe"
  vim.bo[feedback_buffer].swapfile = false
  vim.bo[feedback_buffer].modifiable = false
  vim.bo[feedback_buffer].readonly = true
  vim.wo[feedback_window].number = false
  vim.wo[feedback_window].relativenumber = false
  vim.wo[feedback_window].signcolumn = "no"
  vim.wo[feedback_window].wrap = true
  vim.api.nvim_win_set_cursor(feedback_window, { 1, 0 })

  return feedback_buffer, feedback_window
end

return M
