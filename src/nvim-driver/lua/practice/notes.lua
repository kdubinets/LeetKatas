local M = {}

local config = nil
local NOTE_KINDS = {
  ["follow-up"] = true,
  research = true,
  ["exercise-fix"] = true,
}

local function notify(message, level)
  require("practice.ui").notify(message, level)
end

local function safe_exercise_id(exercise_id)
  local safe = exercise_id:gsub("[^%w._-]", "_")
  return safe ~= "" and safe or "exercise"
end

local function note_body_is_empty(lines)
  local after_heading = false
  for _, line in ipairs(lines) do
    if after_heading and vim.trim(line) ~= "" then
      return false
    end
    if line == "## Note" then
      after_heading = true
    end
  end
  return true
end

local function candidate_path(context, suffix)
  local filename = context.filename_timestamp .. "--" .. safe_exercise_id(context.exercise_id)
  if suffix > 1 then
    filename = filename .. "--" .. suffix
  end
  return config.notes_directory .. "/" .. filename .. ".md"
end

local function write_exclusive(path, lines)
  local contents = table.concat(lines, "\n") .. "\n"
  local descriptor, open_error = vim.uv.fs_open(path, "wx", tonumber("600", 8))
  if not descriptor then
    return false, open_error
  end
  local written, write_error = vim.uv.fs_write(descriptor, contents, -1)
  vim.uv.fs_close(descriptor)
  if written ~= #contents then
    vim.fn.delete(path)
    return false, write_error or "incomplete write"
  end
  return true, nil
end

local function note_lines(context, kind)
  local lines = {
    "# " .. context.exercise_id,
    "",
    "Created: " .. context.created_at,
    "Kind: " .. kind,
    "Collection: " .. context.collection,
    "Exercise: " .. context.exercise_id,
    "Phase: " .. context.phase,
    "Session: " .. context.session_id,
  }
  if context.context then
    table.insert(lines, "Context: " .. context.context)
  end
  if context.section then
    table.insert(lines, "Section: " .. context.section)
  end
  if context.excerpt and context.excerpt ~= "" then
    table.insert(lines, "")
    for _, excerpt_line in ipairs(vim.split(context.excerpt, "\n", { plain = true })) do
      table.insert(lines, "> " .. excerpt_line)
    end
  end
  vim.list_extend(lines, { "", "## Note", "", "" })
  return lines
end

function M.setup(options)
  config = options
end

function M.compose(context, kind)
  kind = kind or "follow-up"
  if not NOTE_KINDS[kind] then
    notify("Unknown note kind: " .. tostring(kind), vim.log.levels.ERROR)
    return nil
  end

  local buffer = vim.api.nvim_create_buf(true, false)
  vim.api.nvim_buf_set_name(buffer, "practice-note://" .. context.filename_timestamp
    .. "/" .. safe_exercise_id(context.exercise_id) .. "/" .. buffer)
  vim.cmd("botright split")
  local composer_window = vim.api.nvim_get_current_win()
  vim.api.nvim_set_current_buf(buffer)
  vim.api.nvim_win_set_height(0, math.max(10, math.floor(vim.o.lines / 3)))
  vim.bo[buffer].buftype = "acwrite"
  vim.bo[buffer].bufhidden = "wipe"
  vim.bo[buffer].filetype = "markdown"
  vim.bo[buffer].swapfile = false
  local lines = note_lines(context, kind)
  vim.api.nvim_buf_set_lines(buffer, 0, -1, false, lines)
  vim.bo[buffer].modified = false
  vim.api.nvim_win_set_cursor(0, { #lines, 0 })
  vim.cmd("startinsert")

  local write_autocmd
  write_autocmd = vim.api.nvim_create_autocmd("BufWriteCmd", {
    buffer = buffer,
    callback = function()
      local current_lines = vim.api.nvim_buf_get_lines(buffer, 0, -1, false)
      if note_body_is_empty(current_lines) then
        notify("Write some note text before saving", vim.log.levels.WARN)
        return
      end
      if vim.fn.mkdir(config.notes_directory, "p") == 0
        and vim.fn.isdirectory(config.notes_directory) == 0
      then
        notify("Could not create notes directory: " .. config.notes_directory,
          vim.log.levels.ERROR)
        return
      end

      local suffix = 1
      local path = candidate_path(context, suffix)
      local saved, save_error = write_exclusive(path, current_lines)
      while not saved and vim.uv.fs_stat(path) do
        suffix = suffix + 1
        path = candidate_path(context, suffix)
        saved, save_error = write_exclusive(path, current_lines)
      end
      if not saved then
        notify("Could not save practice note: " .. tostring(save_error), vim.log.levels.ERROR)
        return
      end

      vim.api.nvim_del_autocmd(write_autocmd)
      vim.bo[buffer].buftype = ""
      vim.bo[buffer].bufhidden = "wipe"
      vim.api.nvim_buf_set_name(buffer, path)
      vim.bo[buffer].modified = false
      notify("Practice note saved: " .. path)
      if vim.api.nvim_win_is_valid(composer_window) then
        vim.api.nvim_win_close(composer_window, true)
      end
    end,
  })

  vim.keymap.set("n", "<C-s>", "<Cmd>write<CR>", {
    buffer = buffer, silent = true, desc = "Save practice note",
  })
  vim.keymap.set("i", "<C-s>", "<Esc><Cmd>write<CR>", {
    buffer = buffer, silent = true, desc = "Save practice note",
  })
  vim.keymap.set("n", "q", "<Cmd>quit<CR>", {
    buffer = buffer, silent = true, desc = "Close practice note",
  })
  return buffer
end

function M.open_directory()
  if vim.fn.mkdir(config.notes_directory, "p") == 0
    and vim.fn.isdirectory(config.notes_directory) == 0
  then
    notify("Could not create notes directory: " .. config.notes_directory,
      vim.log.levels.ERROR)
    return
  end
  local opened, error_message = pcall(vim.cmd.edit, vim.fn.fnameescape(config.notes_directory))
  if not opened then
    notify("Could not open the practice notes directory. Practice notes: " .. config.notes_directory
      .. "\n" .. tostring(error_message), vim.log.levels.WARN)
  end
end

return M
