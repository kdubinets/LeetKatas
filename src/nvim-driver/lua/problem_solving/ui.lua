local M = {}

local brief_buffer, brief_window = nil, nil
local outline_buffer, outline_window = nil, nil
local auxiliary_buffer, auxiliary_window = nil, nil
local outline_namespace = vim.api.nvim_create_namespace("problem-solving-outline")

local function valid_buffer(buffer)
  return buffer and vim.api.nvim_buf_is_valid(buffer)
end

local function valid_window(window)
  return window and vim.api.nvim_win_is_valid(window)
end

local function prepare_buffer(buffer, filetype)
  vim.bo[buffer].buftype = "nofile"
  vim.bo[buffer].bufhidden = "wipe"
  vim.bo[buffer].swapfile = false
  vim.bo[buffer].filetype = filetype
  vim.bo[buffer].modifiable = true
  vim.bo[buffer].readonly = false
end

local function finish_buffer(buffer)
  vim.bo[buffer].modifiable = false
  vim.bo[buffer].readonly = true
end

local function close(buffer, window)
  if valid_window(window) then vim.api.nvim_win_close(window, true) end
  if valid_buffer(buffer) then vim.api.nvim_buf_delete(buffer, { force = true }) end
end

function M.notify(message, level)
  vim.notify(message, level or vim.log.levels.INFO, { title = "Problem Solving" })
end

function M.close_outline()
  close(outline_buffer, outline_window)
  outline_buffer, outline_window = nil, nil
end

function M.close_auxiliary()
  close(auxiliary_buffer, auxiliary_window)
  auxiliary_buffer, auxiliary_window = nil, nil
end


function M.close_all()
  M.close_outline()
  M.close_auxiliary()
  if valid_buffer(brief_buffer) then
    vim.api.nvim_buf_delete(brief_buffer, { force = true })
  end
  brief_buffer, brief_window = nil, nil
end

function M.open_brief(problem, hint)
  M.close_outline()
  M.close_auxiliary()
  if not valid_window(brief_window) then brief_window = vim.api.nvim_get_current_win() end
  if valid_buffer(brief_buffer) then vim.api.nvim_buf_delete(brief_buffer, { force = true }) end
  brief_buffer = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(brief_window, brief_buffer)
  prepare_buffer(brief_buffer, "problem-solving-brief")
  local lines = vim.fn.readfile(problem.brief_path)
  if hint then
    vim.list_extend(lines, { "", "## Optional hint", "", hint })
  end
  vim.api.nvim_buf_set_lines(brief_buffer, 0, -1, false, lines)
  vim.api.nvim_buf_set_name(brief_buffer, "Problem solving: " .. problem.id)
  vim.b[brief_buffer].problem_solving_brief = true
  finish_buffer(brief_buffer)
  vim.wo[brief_window].wrap = true
  vim.wo[brief_window].number = false
  vim.wo[brief_window].relativenumber = false
  vim.api.nvim_set_current_win(brief_window)
  vim.api.nvim_win_set_cursor(brief_window, { 1, 0 })
  return brief_buffer, brief_window
end

function M.open_outline(response)
  M.close_outline()
  if vim.o.columns < 100 then vim.cmd("botright split") else vim.cmd("botright vsplit") end
  outline_window = vim.api.nvim_get_current_win()
  outline_buffer = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(outline_window, outline_buffer)
  prepare_buffer(outline_buffer, "problem-solving-outline")
  local labels = {
    { "Decisive insight", "decisive_insight" },
    { "Approach", "approach" },
    { "State and invariant", "state_and_invariant" },
    { "Correctness", "correctness" },
    { "Complexity", "complexity" },
    { "Pitfall", "pitfall" },
  }
  local lines = { "Solution outline", "" }
  local section_lines = {}
  for _, item in ipairs(labels) do
    table.insert(section_lines, #lines)
    vim.list_extend(lines, { item[1], "", response.solution_outline[item[2]], "" })
  end
  if type(response.accepted_alternatives) == "table" and #response.accepted_alternatives > 0 then
    table.insert(section_lines, #lines)
    vim.list_extend(lines, { "Accepted alternatives", "" })
    for _, alternative in ipairs(response.accepted_alternatives) do
      table.insert(lines, "- " .. alternative)
    end
  end
  vim.api.nvim_buf_set_lines(outline_buffer, 0, -1, false, lines)
  vim.api.nvim_buf_add_highlight(outline_buffer, outline_namespace, "Title", 0, 0, -1)
  for _, line in ipairs(section_lines) do
    vim.api.nvim_buf_add_highlight(outline_buffer, outline_namespace, "Keyword", line, 0, -1)
  end
  vim.api.nvim_buf_set_name(outline_buffer, "Problem-solving outline")
  vim.b[outline_buffer].problem_solving_outline = true
  finish_buffer(outline_buffer)
  vim.wo[outline_window].wrap = true
  -- Keep prose readable in the narrow outline split without wrap glyphs.
  vim.wo[outline_window].linebreak = true
  vim.wo[outline_window].breakindent = true
  vim.wo[outline_window].breakindentopt = "shift:2"
  vim.wo[outline_window].number = false
  vim.wo[outline_window].relativenumber = false
  return outline_buffer, outline_window
end

local function open_auxiliary(title, filetype, lines)
  M.close_auxiliary()
  if vim.o.columns < 100 then vim.cmd("botright split") else vim.cmd("botright vsplit") end
  auxiliary_window = vim.api.nvim_get_current_win()
  auxiliary_buffer = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(auxiliary_window, auxiliary_buffer)
  prepare_buffer(auxiliary_buffer, filetype)
  vim.api.nvim_buf_set_lines(auxiliary_buffer, 0, -1, false, lines)
  vim.api.nvim_buf_set_name(auxiliary_buffer, title)
  finish_buffer(auxiliary_buffer)
  vim.wo[auxiliary_window].wrap = true
  vim.wo[auxiliary_window].number = false
  vim.wo[auxiliary_window].relativenumber = false
  vim.keymap.set("n", "q", M.close_auxiliary,
    { buffer = auxiliary_buffer, silent = true, desc = "Close problem-solving pane" })
  return auxiliary_buffer, auxiliary_window
end

function M.open_bookmarks(bookmarks, reopen)
  local lines = { "# Open-thinking bookmarks", "" }
  if #bookmarks == 0 then
    table.insert(lines, "No problems are bookmarked.")
  else
    for index, bookmark in ipairs(bookmarks) do
      local flags = {}
      if bookmark.hint_requested then table.insert(flags, "hint") end
      if bookmark.revealed then table.insert(flags, "revealed") end
      local suffix = #flags > 0 and " [" .. table.concat(flags, ", ") .. "]" or ""
      table.insert(lines, string.format("%d. %s%s", index, bookmark.problem_id, suffix))
      if bookmark.note and bookmark.note ~= "" then table.insert(lines, "   " .. bookmark.note) end
    end
  end
  local buffer = open_auxiliary("Problem-solving bookmarks", "problem-solving-bookmarks", lines)
  vim.b[buffer].problem_solving_bookmarks = bookmarks
  vim.keymap.set("n", "<CR>", function()
    local line = vim.api.nvim_win_get_cursor(0)[1]
    local index = tonumber((vim.api.nvim_buf_get_lines(buffer, line - 1, line, false)[1] or ""):match("^(%d+)%."))
    if index and bookmarks[index] then reopen(bookmarks[index].problem_id) end
  end, { buffer = buffer, silent = true, desc = "Reopen bookmarked problem" })
  return buffer
end

function M.open_stats(stats)
  local state, reviews = stats.collection_state, stats.reviews
  local lines = {
    "# Problem-solving statistics", "",
    "Collection: " .. stats.collection,
    string.format("Cards: %d total · %d unseen · %d due now · %d due later · %d bookmarked",
      state.total, state.unseen, stats.today.due_now, stats.today.due_later_today,
      state.open_bookmarks),
    string.format("Reviews: %d total · %d problems · %d today · %d new today · Reveals: %d · Hints: %d",
      reviews.total, reviews.problems_total, stats.today.reviews, stats.today.new_reviewed,
      reviews.revealed, reviews.hint_used),
    string.format("Ratings: Again %d · Hard %d · Good %d · Easy %d",
      reviews.ratings.fail, reviews.ratings.acceptable,
      reviews.ratings.good, reviews.ratings.excellent),
  }
  return open_auxiliary("Problem-solving statistics", "problem-solving-stats", lines)
end

function M.open_conversation(history, pending, notice)
  local lines = { "# Problem-solving conversation", "" }
  for index = 1, #history, 2 do
    local question = history[index]
    local answer = history[index + 1]
    if question and question.role == "user" then
      vim.list_extend(lines, { "## You", "", question.content, "" })
    end
    if answer and answer.role == "assistant" then
      vim.list_extend(lines, { "## Coach", "", answer.content, "" })
    end
  end
  if pending then
    vim.list_extend(lines, { "## You", "", pending.question, "", "## Coach", "", "Responding…", "" })
  end
  if notice then
    vim.list_extend(lines, { "## Conversation unavailable", "", notice, "" })
  end
  if #history == 0 and not pending and not notice then
    table.insert(lines, "No conversation yet.")
  end
  local buffer = open_auxiliary(
    "Problem-solving conversation", "problem-solving-conversation", lines
  )
  vim.b[buffer].problem_solving_conversation = true
  return buffer
end

function M.brief_buffer() return brief_buffer end
function M.outline_buffer() return outline_buffer end

return M
