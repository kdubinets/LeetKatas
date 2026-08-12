local M = {}

local brief_buffer, brief_window = nil, nil
local outline_buffer, outline_window = nil, nil
local auxiliary_buffer, auxiliary_window = nil, nil
local stats_buffer, stats_window = nil, nil
local outline_namespace = vim.api.nvim_create_namespace("problem-solving-outline")
local stats_namespace = vim.api.nvim_create_namespace("problem-solving-stats")

vim.api.nvim_set_hl(0, "ProblemSolvingStatsSuccess", { default = true, link = "DiagnosticOk" })
vim.api.nvim_set_hl(0, "ProblemSolvingStatsFailure", { default = true, link = "DiagnosticError" })
vim.api.nvim_set_hl(0, "ProblemSolvingStatsWarning", { default = true, link = "DiagnosticWarn" })
vim.api.nvim_set_hl(0, "ProblemSolvingStatsProgress", { default = true, link = "DiagnosticInfo" })
vim.api.nvim_set_hl(0, "ProblemSolvingStatsHeading", { default = true, link = "Title" })
vim.api.nvim_set_hl(0, "ProblemSolvingStatsHint", { default = true, link = "Comment" })

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

local function title_case(value)
  return value:sub(1, 1):upper() .. value:sub(2)
end

local function humanize_collection(collection)
  local name = collection
  if name:find("/", 1, true) then name = vim.fs.basename(name) end
  local parts = vim.split(name, ".", { plain = true })
  if #parts > 1 and parts[1]:lower() == "leetkatas" then table.remove(parts, 1) end
  for index, part in ipairs(parts) do
    local words = vim.split(part:gsub("[_-]", " "), " ", { trimempty = true })
    for word_index, word in ipairs(words) do words[word_index] = title_case(word:lower()) end
    parts[index] = table.concat(words, " ")
  end
  return table.concat(parts, " ")
end

local function format_duration(milliseconds)
  local minutes = math.floor((math.max(0, milliseconds) + 30000) / 60000)
  if minutes >= 60 then return string.format("%dh %02dm", math.floor(minutes / 60), minutes % 60) end
  return string.format("%dm", minutes)
end

local function parse_date(value)
  local year, month, day = value:match("^(%d%d%d%d)%-(%d%d)%-(%d%d)$")
  if not year then return nil end
  return os.time({ year = tonumber(year), month = tonumber(month), day = tonumber(day), hour = 12 })
end

local function format_date(value, include_year)
  local timestamp = parse_date(value)
  if not timestamp then return value end
  if include_year then
    return string.format("%d %s %s", tonumber(os.date("%d", timestamp)),
      os.date("%b", timestamp), os.date("%Y", timestamp))
  end
  return string.format("%s, %d %s", os.date("%a", timestamp),
    tonumber(os.date("%d", timestamp)), os.date("%b", timestamp))
end

local function bar(value, maximum, width)
  if value == 0 then return "·" end
  local size = math.min(width,
    math.max(1, math.floor((value / math.max(1, maximum)) * width + 0.5)))
  return string.rep("█", size)
end

local function progress_bar(value, total, width)
  local filled = total > 0 and math.floor((value / total) * width + 0.5) or 0
  return string.rep("█", filled) .. string.rep("░", width - filled)
end

local function pad_display(value, width)
  return value .. string.rep(" ", math.max(0, width - vim.fn.strdisplaywidth(value)))
end

local function append_columns(lines, left, right, width)
  local gap = 3
  local left_width = math.floor((width - gap) / 2)
  for index = 1, math.max(#left, #right) do
    table.insert(lines, pad_display(left[index] or "", left_width)
      .. string.rep(" ", gap) .. (right[index] or ""))
  end
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

local function stats_lines(stats, width)
  local today, collection, reviews, forecast = stats.today, stats.collection_state, stats.reviews,
    stats.forecast
  width = math.max(50, width or 76)
  local title, date = "Problem-solving statistics", format_date(today.date, true)
  local lines = {
    pad_display(title, math.max(#title + 2, width - vim.fn.strdisplaywidth(date))) .. date,
    "Collection: " .. humanize_collection(stats.collection),
    "",
  }

  local ratings = today.ratings
  local rating_max = math.max(ratings.fail, ratings.acceptable, ratings.good, ratings.excellent)
  local today_lines = {
    "TODAY",
    string.rep("─", math.max(12, math.floor((width - 3) / 2))),
    string.format("%d reviews completed", today.reviews),
    string.format("%d newly reviewed", today.new_reviewed),
    string.format("%s solving and discussing", format_duration(today.practice_time_ms)),
    "",
    "Ratings",
    string.format("Easy  %3d  %s", ratings.excellent, bar(ratings.excellent, rating_max, 14)),
    string.format("Good  %3d  %s", ratings.good, bar(ratings.good, rating_max, 14)),
    string.format("Hard  %3d  %s", ratings.acceptable, bar(ratings.acceptable, rating_max, 14)),
    string.format("Again %3d  %s", ratings.fail, bar(ratings.fail, rating_max, 14)),
  }
  local percent = collection.total > 0
      and math.floor((collection.introduced / collection.total) * 100 + 0.5) or 0
  local collection_lines = {
    "COLLECTION",
    string.rep("─", math.max(12, math.floor((width - 3) / 2))),
    string.format("%d / %d introduced   %d%%", collection.introduced, collection.total, percent),
    progress_bar(collection.introduced, collection.total, 16),
    "",
    string.format("%d distinct problems reviewed", reviews.problems_total),
    string.format("%d learning", collection.learning),
    string.format("%d learned", collection.learned),
    string.format("%d relearning", collection.relearning),
    string.format("%d unseen", collection.unseen),
    string.format("%d open-thinking bookmarks", collection.open_bookmarks),
  }
  if width >= 70 then
    append_columns(lines, today_lines, collection_lines, width)
  else
    vim.list_extend(lines, today_lines)
    table.insert(lines, "")
    vim.list_extend(lines, collection_lines)
  end

  vim.list_extend(lines, { "", "DUE", string.rep("─", width) })
  table.insert(lines, string.format("  %-18s %3d", "Now", today.due_now))
  table.insert(lines, string.format("  %-18s %3d", "Later today", today.due_later_today))
  local forecast_max = 0
  for _, day in ipairs(forecast.days) do forecast_max = math.max(forecast_max, day.due) end
  for index, day in ipairs(forecast.days) do
    local label = index == 1 and "Tomorrow" or format_date(day.date, false)
    table.insert(lines, string.format("  %-18s %3d  %s", label, day.due,
      bar(day.due, forecast_max, 16)))
  end

  vim.list_extend(lines, { "", "RECENT ACTIVITY", string.rep("─", width) })
  local wide_history = width >= 70
  table.insert(lines, wide_history
      and "  Date          Reviews  New  Again  Hard  Good  Easy  Time"
      or "  Date        Rev New Again Hard Good Easy Time")
  local activity_count = 0
  for _, day in ipairs(stats.history) do
    if day.reviews > 0 and activity_count < 7 then
      activity_count = activity_count + 1
      local label = day.date == today.date and "Today" or format_date(day.date, false)
      if wide_history then
        table.insert(lines, string.format("  %-13s %7d  %3d  %5d  %4d  %4d  %4d  %s",
          label, day.reviews, day.new_reviewed, day.ratings.fail,
          day.ratings.acceptable, day.ratings.good, day.ratings.excellent,
          format_duration(day.practice_time_ms)))
      else
        table.insert(lines, string.format("  %-11s %3d %3d %5d %4d %4d %4d %s",
          label, day.reviews, day.new_reviewed, day.ratings.fail,
          day.ratings.acceptable, day.ratings.good, day.ratings.excellent,
          format_duration(day.practice_time_ms)))
      end
    end
  end
  if activity_count == 0 then table.insert(lines, "  No problem-solving activity yet") end
  table.insert(lines, "")
  table.insert(lines, "[r] Refresh    [q] Close")
  return lines
end

function M.close_stats()
  close(stats_buffer, stats_window)
  stats_buffer, stats_window = nil, nil
end

function M.open_stats(stats, refresh)
  if not valid_window(stats_window) or not valid_buffer(stats_buffer) then
    M.close_stats()
    if vim.o.columns < 110 then vim.cmd("botright split") else vim.cmd("botright vsplit") end
    stats_window = vim.api.nvim_get_current_win()
    stats_buffer = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_win_set_buf(stats_window, stats_buffer)
    if vim.o.columns < 110 then
      vim.api.nvim_win_set_height(stats_window, math.max(12, math.floor(vim.o.lines * 0.55)))
    else
      vim.api.nvim_win_set_width(stats_window, math.min(78, math.max(55, vim.o.columns - 45)))
    end
    prepare_buffer(stats_buffer, "problem-solving-stats")
    vim.wo[stats_window].signcolumn = "no"
    vim.wo[stats_window].wrap = false
    local options = { buffer = stats_buffer, silent = true, nowait = true }
    vim.keymap.set("n", "q", M.close_stats,
      vim.tbl_extend("force", options, { desc = "Close problem-solving statistics" }))
    vim.keymap.set("n", "r", refresh,
      vim.tbl_extend("force", options, { desc = "Refresh problem-solving statistics" }))
  end
  vim.bo[stats_buffer].modifiable = true
  vim.bo[stats_buffer].readonly = false
  local lines = stats_lines(stats, vim.api.nvim_win_get_width(stats_window) - 2)
  vim.api.nvim_buf_set_lines(stats_buffer, 0, -1, false, lines)
  vim.api.nvim_buf_clear_namespace(stats_buffer, stats_namespace, 0, -1)
  for line_number, line in ipairs(lines) do
    if line_number == 1 or line:match("^TODAY") or line:find("COLLECTION", 1, true)
      or line == "DUE" or line == "RECENT ACTIVITY"
    then
      vim.api.nvim_buf_add_highlight(stats_buffer, stats_namespace, "ProblemSolvingStatsHeading",
        line_number - 1, 0, -1)
    elseif line:find("─", 1, true) then
      vim.api.nvim_buf_add_highlight(stats_buffer, stats_namespace, "ProblemSolvingStatsHint",
        line_number - 1, 0, -1)
    end
    for label, group in pairs({
      Easy = "ProblemSolvingStatsSuccess",
      Good = "ProblemSolvingStatsProgress",
      Hard = "ProblemSolvingStatsWarning",
      Again = "ProblemSolvingStatsFailure",
    }) do
      local first, last = line:find(label .. "%s*%d+%s+[█·]+")
      if first then
        vim.api.nvim_buf_add_highlight(stats_buffer, stats_namespace, group,
          line_number - 1, first - 1, last)
      end
    end
  end
  vim.api.nvim_buf_add_highlight(stats_buffer, stats_namespace, "ProblemSolvingStatsHint",
    vim.api.nvim_buf_line_count(stats_buffer) - 1, 0, -1)
  finish_buffer(stats_buffer)
  vim.api.nvim_set_current_win(stats_window)
  return stats_buffer, stats_window
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
