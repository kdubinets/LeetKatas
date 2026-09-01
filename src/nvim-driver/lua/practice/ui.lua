local M = {}
local log = require("practice.log")
local import_folds = require("practice.import_folds")
local completion = require("practice.completion")

local feedback_buffer = nil
local feedback_window = nil
local feedback_namespace = vim.api.nvim_create_namespace("practice_feedback")
local instruction_namespace = vim.api.nvim_create_namespace("practice_instruction")
local source_syntax_namespace = vim.api.nvim_create_namespace("practice_source_syntax")
local next_due_namespace = vim.api.nvim_create_namespace("practice_next_due")
local feedback_contexts = {}
local feedback_result = nil
local feedback_callbacks = nil
local expanded = { review = false, compiler = false, reference = false, chat = true }
local compiler_result, compiler_callbacks = nil, nil
local stats_buffer = nil
local stats_window = nil
local next_due_buffer = nil
local next_due_window = nil
local next_due_timer = nil

local function define_highlights()
  vim.api.nvim_set_hl(0, "PracticeSuccess", { default = true, link = "DiagnosticOk" })
  vim.api.nvim_set_hl(0, "PracticeFailure", { default = true, link = "DiagnosticError" })
  vim.api.nvim_set_hl(0, "PracticeWarning", { default = true, link = "DiagnosticWarn" })
  vim.api.nvim_set_hl(0, "PracticeProgress", { default = true, link = "DiagnosticInfo" })
  vim.api.nvim_set_hl(0, "PracticeHeading", { default = true, link = "Title" })
  vim.api.nvim_set_hl(0, "PracticeHint", { default = true, link = "Comment" })
  vim.api.nvim_set_hl(0, "PracticeRating", { default = true, link = "Special" })
  vim.api.nvim_set_hl(0, "PracticeAction", { default = true, link = "Identifier" })
  vim.api.nvim_set_hl(0, "PracticeInstruction", { default = true, link = "DiagnosticInfo" })
  vim.api.nvim_set_hl(0, "PracticeInstructionLead", { default = true, bold = true, underline = true })
  vim.api.nvim_set_hl(0, "PracticeCode", { default = true, link = "String" })
  vim.api.nvim_set_hl(0, "PracticeCodeBlock", { default = true, link = "PreProc" })
  vim.api.nvim_set_hl(0, "PracticeQuestion", { default = true, link = "DiagnosticInfo" })
  vim.api.nvim_set_hl(0, "PracticeAnswer", { default = true, link = "Normal" })
  vim.api.nvim_set_hl(0, "PracticeQuestionLabel", { default = true, bold = true })
  vim.api.nvim_set_hl(0, "PracticeAnswerLabel", { default = true, bold = true })
  vim.api.nvim_set_hl(0, "PracticeDate", { default = true, fg = "#e5c07b", bold = true })
  vim.api.nvim_set_hl(0, "PracticeTime", { default = true, fg = "#98c379", bold = true })
  -- These deliberately use visible colours rather than linking to the active
  -- theme: several otherwise-good dark themes render all C++ identifiers white.
  vim.api.nvim_set_hl(0, "PracticeSyntaxKeyword", { default = true, fg = "#c678dd", bold = true })
  vim.api.nvim_set_hl(0, "PracticeSyntaxType", { default = true, fg = "#56b6c2" })
  vim.api.nvim_set_hl(0, "PracticeSyntaxFunction", { default = true, fg = "#61afef" })
  vim.api.nvim_set_hl(0, "PracticeSyntaxNamespace", { default = true, fg = "#e5c07b" })
end

define_highlights()

local function valid_buffer(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
end

local function valid_window(window)
  return window ~= nil and vim.api.nvim_win_is_valid(window)
end

local cpp_keywords = {
  ["auto"] = true, ["break"] = true, ["case"] = true, ["class"] = true, ["const"] = true,
  ["constexpr"] = true, ["continue"] = true, ["else"] = true, ["for"] = true,
  ["if"] = true, ["inline"] = true, ["namespace"] = true, ["noexcept"] = true,
  ["private"] = true, ["protected"] = true, ["public"] = true, ["return"] = true,
  ["static"] = true, ["struct"] = true, ["switch"] = true, ["template"] = true,
  ["typename"] = true, ["using"] = true, ["virtual"] = true, ["while"] = true,
}

local cpp_types = {
  ["bool"] = true, ["char"] = true, ["double"] = true, ["float"] = true, ["int"] = true,
  ["long"] = true, ["short"] = true, ["signed"] = true, ["size_t"] = true, ["unsigned"] = true,
  ["void"] = true, ["array"] = true, ["deque"] = true, ["map"] = true, ["optional"] = true,
  ["pair"] = true, ["queue"] = true, ["set"] = true, ["string"] = true, ["tuple"] = true,
  ["unordered_map"] = true, ["unordered_set"] = true, ["vector"] = true,
}

local function add_source_highlight(buffer, line, first, last, group)
  vim.api.nvim_buf_add_highlight(buffer, source_syntax_namespace, group, line, first - 1, last - 1)
end

local function highlight_cpp_source(buffer)
  vim.api.nvim_buf_clear_namespace(buffer, source_syntax_namespace, 0, -1)
  for line_number, text in ipairs(vim.api.nvim_buf_get_lines(buffer, 0, -1, false)) do
    local code = text:match("^(.-)//") or text
    for first, word, last in code:gmatch("()([%a_][%w_]*)()") do
      if cpp_keywords[word] then
        add_source_highlight(buffer, line_number - 1, first, last, "PracticeSyntaxKeyword")
      elseif cpp_types[word] then
        add_source_highlight(buffer, line_number - 1, first, last, "PracticeSyntaxType")
      end
    end
    for first, namespace, last in code:gmatch("()(std)::()") do
      add_source_highlight(buffer, line_number - 1, first, last, "PracticeSyntaxNamespace")
    end
    for first, name in code:gmatch("()([%a_][%w_]*)%s*%(") do
      if not cpp_keywords[name] then
        add_source_highlight(buffer, line_number - 1, first, first + #name,
          "PracticeSyntaxFunction")
      end
    end
  end
end

local function title_case(value)
  return value:sub(1, 1):upper() .. value:sub(2)
end

local function format_duration(milliseconds, tracked, total)
  if total > 0 and tracked == 0 then return "—" end
  local minutes = math.floor((milliseconds + 30000) / 60000)
  local text
  if minutes >= 60 then
    text = string.format("%dh %02dm", math.floor(minutes / 60), minutes % 60)
  else
    text = string.format("%dm", minutes)
  end
  if tracked < total then
    text = string.format("%s (%d/%d tracked)", text, tracked, total)
  end
  return text
end

local function humanize_collection(collection)
  local name = collection
  if name:find("/", 1, true) then name = vim.fs.basename(name) end
  local parts = vim.split(name, ".", { plain = true })
  if #parts > 1 and parts[1]:lower() == "leetkatas" then table.remove(parts, 1) end
  for index, part in ipairs(parts) do
    local words = vim.split(part:gsub("[_-]", " "), " ", { trimempty = true })
    for word_index, word in ipairs(words) do
      if word:lower() == "cpp" then
        words[word_index] = "C++"
      else
        words[word_index] = title_case(word:lower())
      end
    end
    parts[index] = table.concat(words, " ")
  end
  return table.concat(parts, " ")
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

local function days_since_unix_epoch(year, month, day)
  local adjusted_year = year - (month <= 2 and 1 or 0)
  local era = math.floor(adjusted_year / 400)
  local year_of_era = adjusted_year - era * 400
  local month_since_march = month + (month > 2 and -3 or 9)
  local day_of_year = math.floor((153 * month_since_march + 2) / 5) + day - 1
  local day_of_era = year_of_era * 365 + math.floor(year_of_era / 4)
    - math.floor(year_of_era / 100) + day_of_year
  return era * 146097 + day_of_era - 719468
end

local function local_timestamp_parts(value)
  if type(value) ~= "string" then return value end
  local normalized = value:gsub("%.%d+([+-]%d%d:%d%d)$", "%1")
  local year, month, day, hour, minute, second, offset_sign, offset_hour, offset_minute = normalized:match(
    "^(%d%d%d%d)%-(%d%d)%-(%d%d)T(%d%d):(%d%d):(%d%d)([+-])(%d%d):(%d%d)$"
  )
  if not year then return value end
  year, month, day = tonumber(year), tonumber(month), tonumber(day)
  hour, minute, second = tonumber(hour), tonumber(minute), tonumber(second)
  offset_hour, offset_minute = tonumber(offset_hour), tonumber(offset_minute)
  if month < 1 or month > 12 or day < 1 or day > 31 or hour > 23 or minute > 59 or second > 59
    or offset_hour > 23 or offset_minute > 59 then
    return value
  end
  local offset_seconds = (offset_hour * 60 + offset_minute) * 60
  if offset_sign == "-" then offset_seconds = -offset_seconds end
  local timestamp = days_since_unix_epoch(year, month, day) * 86400 + hour * 3600 + minute * 60 + second
    - offset_seconds
  return os.date("%-d %b %Y", timestamp), os.date("%-I:%M %p", timestamp)
end

function M.format_local_timestamp(value)
  local date, time = local_timestamp_parts(value)
  return time and date .. " at " .. time or date
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

local function stats_lines(stats, width)
  local today, collection, forecast = stats.today, stats.collection_state, stats.forecast
  width = math.max(50, width or 76)
  local title, date = "Practice statistics", format_date(today.date, true)
  local lines = {
    pad_display(title, math.max(#title + 2, width - vim.fn.strdisplaywidth(date))) .. date,
    (stats.collection == "portfolio" and "Portfolio" or "Collection: " .. humanize_collection(stats.collection)),
    "",
  }

  local ratings = today.ratings
  local rating_max = math.max(ratings.fail, ratings.acceptable, ratings.good, ratings.excellent)
  local today_lines = {
    "TODAY",
    string.rep("─", math.max(12, math.floor((width - 3) / 2))),
    string.format("%d reviews completed", today.reviews),
    string.format("%s practiced",
      format_duration(today.practice_time_ms, today.tracked_reviews, today.reviews)),
    string.format("%d newly introduced", today.new_introduced),
    "",
    "Ratings",
    string.format("Excellent %3d  %s", ratings.excellent, bar(ratings.excellent, rating_max, 14)),
    string.format("Good      %3d  %s", ratings.good, bar(ratings.good, rating_max, 14)),
    string.format("Acceptable%3d  %s", ratings.acceptable, bar(ratings.acceptable, rating_max, 14)),
    string.format("Fail      %3d  %s", ratings.fail, bar(ratings.fail, rating_max, 14)),
  }
  local percent = collection.total > 0
      and math.floor((collection.introduced / collection.total) * 100 + 0.5) or 0
  local collection_lines = {
    "COLLECTION",
    string.rep("─", math.max(12, math.floor((width - 3) / 2))),
    string.format("%d / %d introduced   %d%%", collection.introduced, collection.total, percent),
    progress_bar(collection.introduced, collection.total, 16),
    "",
    string.format("%d learned", collection.learned),
    string.format("%d learning", collection.learning),
    string.format("%d relearning", collection.relearning),
    "",
    string.format("%d unseen", collection.unseen),
  }
  if width >= 70 then
    append_columns(lines, today_lines, collection_lines, width)
  else
    vim.list_extend(lines, today_lines)
    table.insert(lines, "")
    vim.list_extend(lines, collection_lines)
  end

  if type(stats.collections) == "table" then
    vim.list_extend(lines, { "", "COLLECTION BREAKDOWN", string.rep("─", width) })
    for _, entry in ipairs(stats.collections) do
      local state = entry.collection_state
      table.insert(lines, string.format("  %-30s %3d/%-3d introduced  %3d due  %3d unseen",
        humanize_collection(entry.collection), state.introduced, state.total,
        entry.today.due_now, state.unseen))
    end
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
      and "  Date          Reviews  New  Fail  Accept.  Good  Excl.  Time"
      or "  Date        Rev New Fail Acc Good Excl Time")
  local activity_count = 0
  for _, day in ipairs(stats.history) do
    if day.reviews > 0 and activity_count < 7 then
      activity_count = activity_count + 1
      local label = day.date == today.date and "Today" or format_date(day.date, false)
      local duration = format_duration(day.practice_time_ms, day.tracked_reviews, day.reviews)
      if wide_history then
        table.insert(lines, string.format("  %-13s %7d  %3d  %4d  %7d  %4d  %5d  %s",
          label, day.reviews, day.new_introduced, day.ratings.fail,
          day.ratings.acceptable, day.ratings.good, day.ratings.excellent, duration))
      else
        table.insert(lines, string.format("  %-11s %3d %3d %4d %3d %4d %4d %s",
          label, day.reviews, day.new_introduced, day.ratings.fail,
          day.ratings.acceptable, day.ratings.good, day.ratings.excellent, duration))
      end
    end
  end
  if activity_count == 0 then table.insert(lines, "  No practice activity yet") end
  if type(stats.reviewer_usage) == "table" and #stats.reviewer_usage > 0 then
    vim.list_extend(lines, { "", "REVIEWER LATENCY", string.rep("─", width) })
    table.insert(lines, "  Provider / model / effort / tier                         Calls  Avg     Cost")
    for _, item in ipairs(stats.reviewer_usage) do
      local label = string.format("%s / %s / %s / %s", item.provider, item.model,
        item.reasoning_effort, item.service_tier)
      local average = item.reviews > 0 and math.floor(item.feedback_duration_ms / item.reviews + 0.5) or 0
      local cost = type(item.estimated_cost_microusd) == "number"
        and string.format("$%.4f", item.estimated_cost_microusd / 1000000) or "—"
      table.insert(lines, string.format("  %-58s %5d  %.1fs  %s", label, item.reviews,
        average / 1000, cost))
    end
  end
  table.insert(lines, "")
  table.insert(lines, "[r] Refresh    [q] Close")
  return lines
end

local function clean_inline(value)
  value = tostring(value or "")
  value = value:gsub("%*%*(.-)%*%*", "%1"):gsub("__(.-)__", "%1")
  value = value:gsub("^%s*#+%s*", ""):gsub("^%s*[-*+]%s+", "")
  value = value:gsub("`([^`]+)`", "%1")
  return value
end

local function clean_inline_ranges(value)
  value = tostring(value or "")
  value = value:gsub("%*%*(.-)%*%*", "%1"):gsub("__(.-)__", "%1")
  value = value:gsub("^%s*#+%s*", ""):gsub("^%s*[-*+]%s+", "")
  local output, ranges, cursor = "", {}, 1
  while true do
    local first, last, code = value:find("`([^`]+)`", cursor)
    if not first then
      output = output .. value:sub(cursor)
      break
    end
    output = output .. value:sub(cursor, first - 1)
    local start_column = #output
    output = output .. code
    table.insert(ranges, { start_column, #output })
    cursor = last + 1
  end
  return output, ranges
end

local function add_line(render, text, context, highlight)
  local normalized = tostring(text or ""):gsub("\r\n?", "\n")
  for _, line in ipairs(vim.split(normalized, "\n", { plain = true })) do
    table.insert(render.lines, line)
    render.contexts[#render.lines] = context or render.contexts[#render.lines - 1]
    if highlight then
      table.insert(render.highlights, { #render.lines - 1, 0, -1, highlight })
    end
  end
end

local function add_text(render, text, context, highlight)
  for _, line in ipairs(vim.split(tostring(text or ""), "\n", { plain = true })) do
    local cleaned, ranges = clean_inline_ranges(line)
    add_line(render, cleaned, context, highlight)
    for _, range in ipairs(ranges) do
      table.insert(render.highlights, { #render.lines - 1, range[1], range[2], "PracticeCode" })
    end
  end
end

local function blank(render)
  if #render.lines > 0 and render.lines[#render.lines] ~= "" then
    add_line(render, "")
  end
end

local function add_heading(render, title, id, suffix)
  blank(render)
  render.positions[id] = #render.lines + 1
  add_line(render, title .. (suffix or ""), { section = title, logical_section = id },
    "PracticeHeading")
end

local function outcome(result)
  local review = result.review
  if result.gave_up then
    return "Gave up", "PracticeFailure", nil
  end
  local feedback = type(review) == "table" and review.status == "available"
      and type(review.feedback) == "table" and review.feedback or nil
  if not feedback or feedback.verdict == "cannot_assess" then
    return "Review unavailable", "PracticeWarning", feedback
  end
  if result.compiled and feedback.verdict == "correct" then
    return "Correct", "PracticeSuccess", feedback
  elseif feedback.verdict == "minor_defect" then
    return "Almost there", "PracticeWarning", feedback
  end
  return "Needs another attempt", "PracticeFailure", feedback
end

local function add_code(render, code, context)
  for _, line in ipairs(vim.split(tostring(code or ""), "\n", { plain = true })) do
    add_line(render, "    " .. line, context, "PracticeCodeBlock")
  end
end

local function add_issues(render, title, issues)
  if type(issues) ~= "table" or #issues == 0 then return end
  add_line(render, title, { section = "Detailed review", logical_section = "review" },
    "PracticeHeading")
  for _, issue in ipairs(issues) do
    add_line(render, "  • " .. clean_inline(issue),
      { section = "Detailed review", logical_section = "review" })
  end
  blank(render)
end

local function add_follow_up_chat(render, result)
  local follow_up = type(result.follow_up) == "table" and result.follow_up or nil
  local turns = follow_up and type(follow_up.turns) == "table" and follow_up.turns or {}
  if #turns == 0 then return end

  local suffix = expanded.chat and "  [t collapse]" or "  [t expand]"
  add_heading(render, "Follow-up chat", "chat", suffix)
  if not expanded.chat then return end

  for _, turn in ipairs(turns) do
    add_line(render, "You", { section = "Follow-up chat", logical_section = "chat" },
      "PracticeQuestionLabel")
    add_text(render, turn.question or "", { section = "Follow-up chat", logical_section = "chat" },
      "PracticeQuestion")
    blank(render)

    local reviewer = type(turn.reviewer) == "string" and turn.reviewer or "Reviewer"
    local model = type(turn.model) == "string" and " · " .. turn.model or ""
    add_line(render, reviewer .. model,
      { section = "Follow-up chat", logical_section = "chat" }, "PracticeAnswerLabel")
    if turn.status == "pending" then
      add_line(render, "Responding…", { section = "Follow-up chat", logical_section = "chat" },
        "PracticeProgress")
    elseif turn.status == "failed" then
      add_text(render, turn.failure or "Follow-up response unavailable.",
        { section = "Follow-up chat", logical_section = "chat" }, "PracticeWarning")
    else
      add_text(render, turn.answer or "", { section = "Follow-up chat", logical_section = "chat" },
        "PracticeAnswer")
    end
    blank(render)
  end
end

local function add_reference(render, result)
  local sections = type(result.metadata_sections) == "table" and result.metadata_sections or {}
  if #sections > 0 then
    for _, section in ipairs(sections) do
      local section_context = { section = "Exercise reference — " .. tostring(section.title),
        logical_section = "reference", metadata_line = section.heading_line }
      add_line(render, clean_inline(section.title), section_context, "PracticeHeading")
      for _, block in ipairs(type(section.blocks) == "table" and section.blocks or {}) do
        if type(block.lines) == "table" then
          for offset, line in ipairs(block.lines) do
            local context = { section = "Exercise reference — " .. tostring(section.title),
              logical_section = "reference", metadata_line = block.start_line + offset - 1 }
            if block.type == "code" then
              add_line(render, "    " .. tostring(line), context, "PracticeCodeBlock")
            else
              add_line(render, clean_inline(line), context)
            end
          end
        end
      end
      blank(render)
    end
    return
  end

  -- Legacy or malformed metadata remains readable without Markdown delimiters.
  local in_fence = false
  for line_number, line in ipairs(vim.split(result.metadata or "", "\n", { plain = true })) do
    if line:match("^%s*```") then
      in_fence = not in_fence
    else
      local context = { section = "Exercise reference", logical_section = "reference",
        metadata_line = line_number }
      add_line(render, (in_fence and "    " or "") .. clean_inline(line), context,
        in_fence and "PracticeCodeBlock" or nil)
    end
  end
end

local function build_feedback(result)
  local render = { lines = {}, contexts = {}, highlights = {}, positions = {} }
  local status, status_highlight, review = outcome(result)
  local rating = type(result.proposed_rating) == "string" and title_case(result.proposed_rating) or nil
  render.positions.outcome = 1
  add_line(render, status .. (rating and "  [" .. rating .. "]" or ""),
    { section = "Outcome", logical_section = "outcome" }, status_highlight)
  if rating then
    local start = #status + 2
    table.insert(render.highlights, { 0, start, -1, "PracticeRating" })
  end

  if review and type(review.summary) == "string" and review.summary ~= "" then
    blank(render)
    add_text(render, review.summary, { section = "Summary", logical_section = "summary" })
  elseif type(result.review) == "table" and result.review.failure then
    blank(render)
    add_line(render, result.gave_up
        and "Compilation and reviewer assessment were skipped. The reference is shown below; ask follow-up questions if useful."
        or "Structured review is unavailable. Choose a manual rating.",
      { section = "Summary", logical_section = "summary" }, "PracticeWarning")
  end

  if not result.compiled and rating and result.proposed_rating ~= "fail" then
    blank(render)
    add_line(render, "The reviewer recognized the approach, but this submission did not compile.",
      { section = "Summary", logical_section = "summary" }, "PracticeHint")
  end

  if review and (review.verdict == "minor_defect" or review.verdict == "incorrect") then
    add_heading(render, "Correction", "correction")
    if type(review.improved_implementation) == "string" and review.improved_implementation ~= "" then
      add_code(render, review.improved_implementation,
        { section = "Correction", logical_section = "correction" })
    end
    if type(review.improvement_explanation) == "string" and review.improvement_explanation ~= "" then
      blank(render)
      add_text(render, review.improvement_explanation,
        { section = "Correction", logical_section = "correction" })
    end
  end

  add_heading(render, "Actions", "actions")
  if rating then
    add_line(render, "Primary   a / <Space>a  Accept " .. rating .. " and continue",
      { section = "Actions", logical_section = "actions" }, "PracticeAction")
    add_line(render, "Stay      S / <Space>R  Accept " .. rating .. " and keep editing",
      { section = "Actions", logical_section = "actions" }, "PracticeAction")
  else
    add_line(render, "Primary   Choose a manual rating to continue",
      { section = "Actions", logical_section = "actions" }, "PracticeWarning")
  end
  add_line(render, "Ratings   1 Fail   2 Acceptable   3 Good   4 Excellent",
    { section = "Actions", logical_section = "actions" }, "PracticeAction")
  add_line(render, "More      ? Ask reviewer   m Note   n Skip",
    { section = "Actions", logical_section = "actions" }, "PracticeAction")
  local details = { "d Review" }
  if type(result.diagnostics) == "string" and result.diagnostics ~= "" then
    table.insert(details, "c Compiler")
  end
  table.insert(details, "r Reference")
  local follow_up = type(result.follow_up) == "table" and result.follow_up or nil
  if follow_up and type(follow_up.turns) == "table" and #follow_up.turns > 0 then
    table.insert(details, "t Chat")
  end
  add_line(render, "Details   " .. table.concat(details, "   "),
    { section = "Actions", logical_section = "actions" }, "PracticeAction")

  add_follow_up_chat(render, result)

  local review_suffix = expanded.review and "  [d collapse]" or "  [d expand]"
  add_heading(render, "Detailed review", "review", review_suffix)
  if expanded.review then
    if review then
      if type(review.correctness_analysis) == "string" and review.correctness_analysis ~= "" then
        add_line(render, "Correctness", { section = "Detailed review", logical_section = "review" },
          "PracticeHeading")
        add_text(render, review.correctness_analysis,
          { section = "Detailed review", logical_section = "review" })
        blank(render)
      end
      add_issues(render, "Major issues", review.major_issues)
      add_issues(render, "Minor issues", review.minor_issues)
      if type(review.code_quality_analysis) == "string" and review.code_quality_analysis ~= "" then
        add_line(render, "Code quality", { section = "Detailed review", logical_section = "review" },
          "PracticeHeading")
        add_text(render, review.code_quality_analysis,
          { section = "Detailed review", logical_section = "review" })
        blank(render)
      end
      if type(review.rating_explanation) == "string" and review.rating_explanation ~= "" then
        add_line(render, "Rating rationale", { section = "Detailed review", logical_section = "review" },
          "PracticeHeading")
        add_text(render, review.rating_explanation,
          { section = "Detailed review", logical_section = "review" })
        blank(render)
      end
      if type(review.version_notes) == "string" and review.version_notes ~= "" then
        add_line(render, "Version notes", { section = "Detailed review", logical_section = "review" },
          "PracticeHeading")
        add_text(render, review.version_notes,
          { section = "Detailed review", logical_section = "review" })
        blank(render)
      end
      if review.verdict == "correct" and type(review.improved_implementation) == "string"
          and review.improved_implementation ~= "" then
        add_line(render, "Improved implementation",
          { section = "Detailed review", logical_section = "review" }, "PracticeHeading")
        add_code(render, review.improved_implementation,
          { section = "Detailed review", logical_section = "review" })
        add_text(render, review.improvement_explanation or "",
          { section = "Detailed review", logical_section = "review" })
        blank(render)
      end
      if type(review.alternative_implementation) == "string"
          and review.alternative_implementation ~= "" then
        add_line(render, "Alternative implementation",
          { section = "Detailed review", logical_section = "review" }, "PracticeHeading")
        add_code(render, review.alternative_implementation,
          { section = "Detailed review", logical_section = "review" })
        add_text(render, review.alternative_explanation or "",
          { section = "Detailed review", logical_section = "review" })
      end
      add_line(render, "Reviewer: " .. tostring(result.review.reviewer or "unknown")
          .. (type(result.review.model) == "string" and " · " .. result.review.model or ""),
        { section = "Detailed review", logical_section = "review" }, "PracticeHint")
    else
      add_line(render, clean_inline(result.review.failure or "No structured review was returned."),
        { section = "Detailed review", logical_section = "review" }, "PracticeWarning")
    end
  end

  if type(result.diagnostics) == "string" and result.diagnostics ~= "" then
    local suffix = expanded.compiler and "  [c collapse]" or "  [c expand]"
    add_heading(render, "Compiler details", "compiler", suffix)
    if expanded.compiler then
      add_code(render, result.diagnostics,
        { section = "Compiler details", logical_section = "compiler" })
    end
  end

  local reference_suffix = expanded.reference and "  [r collapse]" or "  [r expand]"
  add_heading(render, "Exercise reference", "reference", reference_suffix)
  if expanded.reference then add_reference(render, result) end
  return render
end

local function build_compiler_result(result)
  local render = { lines = {}, contexts = {}, highlights = {}, positions = {} }
  add_line(render, result.compiled and "Compilation succeeded" or "Compilation failed",
    { section = "Compiler result", logical_section = "compiler" },
    result.compiled and "PracticeSuccess" or "PracticeFailure")
  blank(render)
  if result.diagnostics ~= "" then
    add_heading(render, "Compiler diagnostics", "compiler")
    add_code(render, result.diagnostics, { section = "Compiler diagnostics", logical_section = "compiler" })
  else
    add_line(render, "The compiler reported no diagnostics.",
      { section = "Compiler result", logical_section = "compiler" }, "PracticeHint")
  end
  add_heading(render, "Actions", "actions")
  add_line(render, "? Ask LLM about these diagnostics   q Close pane",
    { section = "Actions", logical_section = "actions" }, "PracticeAction")
  local chat = result.chat and result.chat.turns or {}
  if #chat > 0 then
    add_heading(render, "Compiler questions", "chat")
    for _, turn in ipairs(chat) do
      add_line(render, "You: " .. turn.question, { section = "Compiler questions", logical_section = "chat" }, "PracticeQuestion")
      add_text(render, turn.status == "available" and turn.answer or (turn.failure or "Waiting for explanation…"),
        { section = "Compiler questions", logical_section = "chat" },
        turn.status == "available" and nil or "PracticeWarning")
      blank(render)
    end
  end
  return render
end

local function set_feedback_lines(render)
  if not valid_buffer(feedback_buffer) then return end
  vim.bo[feedback_buffer].modifiable = true
  vim.bo[feedback_buffer].readonly = false
  vim.api.nvim_buf_set_lines(feedback_buffer, 0, -1, false, render.lines)
  vim.bo[feedback_buffer].filetype = "practice-feedback"
  vim.bo[feedback_buffer].buftype = "nofile"
  vim.bo[feedback_buffer].bufhidden = "wipe"
  vim.bo[feedback_buffer].swapfile = false
  vim.api.nvim_buf_clear_namespace(feedback_buffer, feedback_namespace, 0, -1)
  for _, mark in ipairs(render.highlights) do
    vim.api.nvim_buf_add_highlight(feedback_buffer, feedback_namespace,
      mark[4], mark[1], mark[2], mark[3])
  end
  feedback_contexts = render.contexts
  vim.bo[feedback_buffer].modifiable = false
  vim.bo[feedback_buffer].readonly = true
end

local function ensure_feedback(source_window, focus_feedback)
  if valid_window(feedback_window) and valid_buffer(feedback_buffer) then
    if focus_feedback then vim.api.nvim_set_current_win(feedback_window) end
    return
  end
  M.close_feedback()
  if valid_window(source_window) then vim.api.nvim_set_current_win(source_window) end
  if vim.o.columns < 120 then vim.cmd("botright split") else vim.cmd("botright vsplit") end
  feedback_window = vim.api.nvim_get_current_win()
  feedback_buffer = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(feedback_window, feedback_buffer)
  if vim.o.columns < 120 then
    vim.api.nvim_win_set_height(feedback_window, math.max(10, math.floor(vim.o.lines * 0.45)))
  else
    local available = math.max(40, vim.o.columns - 40)
    vim.api.nvim_win_set_width(feedback_window,
      math.min(math.max(52, math.floor(vim.o.columns * 0.40)), available))
  end
  vim.wo[feedback_window].number = false
  vim.wo[feedback_window].relativenumber = false
  vim.wo[feedback_window].signcolumn = "no"
  vim.wo[feedback_window].wrap = true
  vim.wo[feedback_window].linebreak = true
  vim.wo[feedback_window].breakindent = true
  if not focus_feedback and valid_window(source_window) then
    vim.api.nvim_set_current_win(source_window)
  end
end

local function render_feedback(cursor_section)
  if not feedback_result or not valid_buffer(feedback_buffer) then return end
  local render = build_feedback(feedback_result)
  set_feedback_lines(render)
  if valid_window(feedback_window) then
    local line = render.positions[cursor_section or "outcome"] or 1
    vim.api.nvim_win_set_cursor(feedback_window, { line, 0 })
  end
  return render
end

local function toggle(name)
  expanded[name] = not expanded[name]
  render_feedback(name)
end

local function callback(name, ...)
  local fn = feedback_callbacks and feedback_callbacks[name]
  if fn then fn(...) end
end

local function install_feedback_mappings()
  local options = { buffer = feedback_buffer, silent = true, nowait = true }
  vim.keymap.set("n", "a", function() callback("accept") end,
    vim.tbl_extend("force", options, { desc = "Accept proposed rating" }))
  vim.keymap.set("n", "S", function() callback("accept_stay") end,
    vim.tbl_extend("force", options, { desc = "Accept proposed rating and keep editing" }))
  local ratings = { "fail", "acceptable", "good", "excellent" }
  for index, rating in ipairs(ratings) do
    vim.keymap.set("n", tostring(index), function() callback("rate", rating) end,
      vim.tbl_extend("force", options, { desc = "Record " .. title_case(rating) }))
  end
  vim.keymap.set("n", "n", function() callback("skip") end,
    vim.tbl_extend("force", options, { desc = "Skip without recording" }))
  vim.keymap.set("n", "m", function() callback("note") end,
    vim.tbl_extend("force", options, { desc = "Capture feedback note" }))
  vim.keymap.set("n", "d", function() toggle("review") end,
    vim.tbl_extend("force", options, { desc = "Toggle detailed review" }))
  vim.keymap.set("n", "c", function() toggle("compiler") end,
    vim.tbl_extend("force", options, { desc = "Toggle compiler details" }))
  vim.keymap.set("n", "r", function() toggle("reference") end,
    vim.tbl_extend("force", options, { desc = "Toggle exercise reference" }))
  vim.keymap.set("n", "t", function() toggle("chat") end,
    vim.tbl_extend("force", options, { desc = "Toggle follow-up chat" }))
  vim.keymap.set("n", "?", function() callback("ask") end,
    vim.tbl_extend("force", options, { desc = "Ask the reviewer a follow-up question" }))
  vim.keymap.set("n", "<CR>", function()
    local _, _, review = outcome(feedback_result)
    if type(feedback_result.proposed_rating) ~= "string" then
      M.notify("No reviewer rating is available; choose a manual rating", vim.log.levels.WARN)
    elseif review and review.verdict == "correct" and feedback_result.compiled then
      callback("accept")
    else
      callback("retry")
    end
  end, vim.tbl_extend("force", options, { desc = "Default feedback action" }))
end

function M.notify(message, level)
  log.event("notification", level == vim.log.levels.ERROR and "error" or "info",
    { message = message, nvim_level = level })
  vim.notify(message, level or vim.log.levels.INFO, { title = "Practice" })
end

local function close_next_due_notification()
  if next_due_timer then
    next_due_timer:stop()
    if not next_due_timer:is_closing() then next_due_timer:close() end
  end
  if valid_window(next_due_window) then vim.api.nvim_win_close(next_due_window, true) end
  if valid_buffer(next_due_buffer) then vim.api.nvim_buf_delete(next_due_buffer, { force = true }) end
  next_due_buffer, next_due_window, next_due_timer = nil, nil, nil
end

function M.notify_next_due(value, prefix)
  local date, time = local_timestamp_parts(value)
  prefix = prefix or "No exercises are due. Next review: "
  if not time then
    M.notify(prefix .. tostring(date))
    return
  end

  close_next_due_notification()
  local message = " " .. prefix .. date .. " at " .. time .. " "
  local width = math.min(vim.fn.strdisplaywidth(message), math.max(1, vim.o.columns - 4))
  next_due_buffer = vim.api.nvim_create_buf(false, true)
  vim.bo[next_due_buffer].bufhidden = "wipe"
  vim.bo[next_due_buffer].modifiable = true
  vim.api.nvim_buf_set_lines(next_due_buffer, 0, -1, false, { message })
  vim.bo[next_due_buffer].modifiable = false
  vim.api.nvim_buf_add_highlight(next_due_buffer, next_due_namespace, "PracticeProgress", 0, 1, #prefix + 1)
  vim.api.nvim_buf_add_highlight(next_due_buffer, next_due_namespace, "PracticeDate", 0, #prefix + 1,
    #prefix + #date + 1)
  vim.api.nvim_buf_add_highlight(next_due_buffer, next_due_namespace, "PracticeTime", 0,
    #prefix + #date + 5, #message - 1)
  next_due_window = vim.api.nvim_open_win(next_due_buffer, false, {
    relative = "editor",
    anchor = "NW",
    row = 1,
    col = vim.o.columns - width - 2,
    width = width,
    height = 1,
    focusable = false,
    style = "minimal",
    border = "rounded",
    zindex = 200,
  })
  vim.wo[next_due_window].wrap = false
  vim.wo[next_due_window].winhighlight = "Normal:NormalFloat,FloatBorder:FloatBorder"
  log.event("notification", "info", { message = message, nvim_level = vim.log.levels.INFO })
  next_due_timer = vim.defer_fn(close_next_due_notification, 8000)
  return next_due_buffer
end

function M.confirm_discard(action)
  return vim.fn.confirm("The current attempt has unsaved changes. Discard them and " .. action .. "?",
    "&Discard\n&Cancel", 2) == 1
end

function M.close_feedback()
  if valid_window(feedback_window) then vim.api.nvim_win_close(feedback_window, true) end
  if valid_buffer(feedback_buffer) then vim.api.nvim_buf_delete(feedback_buffer, { force = true }) end
  feedback_window, feedback_buffer = nil, nil
  feedback_contexts, feedback_result, feedback_callbacks = {}, nil, nil
  compiler_result, compiler_callbacks = nil, nil
  expanded = { review = false, compiler = false, reference = false, chat = true }
end

function M.open_compiler_result(source_window, result, callbacks)
  ensure_feedback(source_window, false)
  compiler_result, compiler_callbacks = result, callbacks or {}
  local render = build_compiler_result(result)
  set_feedback_lines(render)
  local options = { buffer = feedback_buffer, silent = true, nowait = true }
  vim.keymap.set("n", "?", function()
    if compiler_callbacks.ask then compiler_callbacks.ask() end
  end, vim.tbl_extend("force", options, { desc = "Ask about compiler diagnostics" }))
  vim.keymap.set("n", "q", M.close_feedback,
    vim.tbl_extend("force", options, { desc = "Close compiler results" }))
  return feedback_buffer, feedback_window
end

function M.refresh_compiler_result()
  if compiler_result and valid_buffer(feedback_buffer) then
    set_feedback_lines(build_compiler_result(compiler_result))
  end
end

function M.close_stats()
  if valid_window(stats_window) then vim.api.nvim_win_close(stats_window, true) end
  if valid_buffer(stats_buffer) then vim.api.nvim_buf_delete(stats_buffer, { force = true }) end
  stats_window, stats_buffer = nil, nil
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
    vim.bo[stats_buffer].filetype = "practice-stats"
    vim.bo[stats_buffer].buftype = "nofile"
    vim.bo[stats_buffer].bufhidden = "wipe"
    vim.bo[stats_buffer].swapfile = false
    vim.wo[stats_window].number = false
    vim.wo[stats_window].relativenumber = false
    vim.wo[stats_window].signcolumn = "no"
    vim.wo[stats_window].wrap = false
    local options = { buffer = stats_buffer, silent = true, nowait = true }
    vim.keymap.set("n", "q", M.close_stats,
      vim.tbl_extend("force", options, { desc = "Close practice statistics" }))
    vim.keymap.set("n", "r", refresh,
      vim.tbl_extend("force", options, { desc = "Refresh practice statistics" }))
  end
  vim.bo[stats_buffer].modifiable = true
  vim.bo[stats_buffer].readonly = false
  local width = vim.api.nvim_win_get_width(stats_window) - 2
  local lines = stats_lines(stats, width)
  vim.api.nvim_buf_set_lines(stats_buffer, 0, -1, false, lines)
  vim.api.nvim_buf_clear_namespace(stats_buffer, feedback_namespace, 0, -1)
  for line_number, line in ipairs(lines) do
    if line_number == 1 or line:match("^TODAY") or line:find("COLLECTION", 1, true)
      or line == "DUE" or line == "RECENT ACTIVITY"
    then
      vim.api.nvim_buf_add_highlight(stats_buffer, feedback_namespace, "PracticeHeading",
        line_number - 1, 0, -1)
    elseif line:find("─", 1, true) then
      vim.api.nvim_buf_add_highlight(stats_buffer, feedback_namespace, "PracticeHint",
        line_number - 1, 0, -1)
    end
    for label, group in pairs({
      Excellent = "PracticeSuccess",
      Good = "PracticeProgress",
      Acceptable = "PracticeWarning",
      Fail = "PracticeFailure",
    }) do
      local first, last = line:find(label .. "%s*%d+%s+[█·]+")
      if first then
        vim.api.nvim_buf_add_highlight(stats_buffer, feedback_namespace, group,
          line_number - 1, first - 1, last)
      end
    end
  end
  vim.api.nvim_buf_add_highlight(stats_buffer, feedback_namespace, "PracticeHint",
    vim.api.nvim_buf_line_count(stats_buffer) - 1, 0, -1)
  vim.bo[stats_buffer].modifiable = false
  vim.bo[stats_buffer].readonly = true
  vim.api.nvim_set_current_win(stats_window)
  return stats_buffer, stats_window
end

function M.open_source(path, preferred_window, practice_marker, enhanced_syntax_highlighting,
                       local_completion)
  M.close_feedback()
  if valid_window(preferred_window) then vim.api.nvim_set_current_win(preferred_window) end
  vim.cmd("edit! " .. vim.fn.fnameescape(path))
  local buffer, window = vim.api.nvim_get_current_buf(), vim.api.nvim_get_current_win()
  vim.bo[buffer].bufhidden = "wipe"
  vim.bo[buffer].swapfile = false
  vim.bo[buffer].completefunc, vim.bo[buffer].omnifunc, vim.bo[buffer].tagfunc = "", "", ""
  if local_completion then completion.enable(buffer) end
  if enhanced_syntax_highlighting then
    local started = vim.treesitter and type(vim.treesitter.start) == "function"
      and pcall(vim.treesitter.start, buffer)
    if not started and vim.bo[buffer].filetype == "cpp" then
      highlight_cpp_source(buffer)
      vim.api.nvim_create_autocmd({ "TextChanged", "TextChangedI" }, {
        buffer = buffer,
        callback = function() highlight_cpp_source(buffer) end,
        desc = "Keep fallback C++ practice syntax highlighting current",
      })
    end
  end
  import_folds.close(buffer, window)
  for index, line in ipairs(vim.api.nvim_buf_get_lines(buffer, 0, -1, false)) do
    local marker_start = line:find(practice_marker, 1, true)
    if marker_start then
      local marker_column = marker_start - 1
      vim.api.nvim_buf_set_extmark(buffer, instruction_namespace, index - 1, marker_column, {
        end_col = #line,
        hl_group = "PracticeInstruction",
        priority = 200,
      })
      vim.api.nvim_buf_set_extmark(buffer, instruction_namespace, index - 1, marker_column, {
        end_col = marker_column + #practice_marker,
        hl_group = "PracticeInstructionLead",
        hl_mode = "combine",
        priority = 201,
      })
      vim.api.nvim_win_set_cursor(window, { index, marker_column })
      break
    end
  end
  return buffer, window
end

function M.open_feedback(source_window, result, callbacks)
  ensure_feedback(source_window, true)
  feedback_result, feedback_callbacks = result, callbacks or {}
  local _, _, review = outcome(result)
  local has_improved_implementation = review ~= nil
    and type(review.improved_implementation) == "string"
    and review.improved_implementation ~= ""
  local has_version_notes = review ~= nil
    and type(review.version_notes) == "string"
    and review.version_notes ~= ""
  expanded.review = result.proposed_rating ~= "excellent"
    or has_improved_implementation or has_version_notes
  expanded.reference = result.gave_up == true
  local render = render_feedback("outcome")
  local rendered_improved_section, rendered_version_section = false, false
  for _, line in ipairs(render and render.lines or {}) do
    if line == "Improved implementation" then rendered_improved_section = true end
    if line == "Version notes" then rendered_version_section = true end
  end
  local buffer_improved_section, buffer_version_section = false, false
  if valid_buffer(feedback_buffer) then
    for _, line in ipairs(vim.api.nvim_buf_get_lines(feedback_buffer, 0, -1, false)) do
      if line == "Improved implementation" then buffer_improved_section = true end
      if line == "Version notes" then buffer_version_section = true end
    end
  end
  log.event("feedback_opened", "info", {
    proposed_rating = type(result.proposed_rating) == "string" and result.proposed_rating or nil,
    review_status = type(result.review) == "table" and result.review.status or nil,
    review_verdict = review and review.verdict or nil,
    review_started_collapsed = not expanded.review,
    has_improved_implementation = has_improved_implementation,
    has_version_notes = has_version_notes,
    rendered_improved_section = rendered_improved_section,
    rendered_version_section = rendered_version_section,
    buffer_improved_section = buffer_improved_section,
    buffer_version_section = buffer_version_section,
    feedback_window_displays_buffer = valid_window(feedback_window)
      and vim.api.nvim_win_get_buf(feedback_window) == feedback_buffer,
  })
  install_feedback_mappings()
  return feedback_buffer, feedback_window
end

function M.open_progress(source_window)
  ensure_feedback(source_window, false)
  M.update_progress(0, {})
  return feedback_buffer, feedback_window
end

function M.refresh_feedback(cursor_section)
  render_feedback(cursor_section)
end

function M.update_progress(elapsed_seconds, events)
  if not valid_buffer(feedback_buffer) then return end
  local frames = { "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏" }
  local frame = frames[(math.floor(elapsed_seconds * 10) % #frames) + 1]
  local compilation, attempt, retry_delay, review_finished, failure_category = nil, nil, nil, nil, nil
  local maximum_attempts = 3
  for _, event in ipairs(events) do
    if event.event == "compilation_finished" then compilation = event.compiled
    elseif event.event == "review_attempt_started" then
      attempt, maximum_attempts, retry_delay = event.attempt,
        event.maximum_attempts or maximum_attempts, nil
    elseif event.event == "review_attempt_failed" then failure_category = event.failure_category
    elseif event.event == "review_retry_scheduled" then retry_delay = event.delay_seconds
    elseif event.event == "review_finished" then review_finished = event.status end
  end
  local render = { lines = {}, contexts = {}, highlights = {}, positions = {} }
  add_line(render, "Practice evaluation", { section = "Practice evaluation" }, "PracticeHeading")
  add_line(render, string.format("%s Working… %.1fs", frame, elapsed_seconds),
    { section = "Practice evaluation" }, "PracticeProgress")
  blank(render)
  add_line(render, "✓ Source saved", { section = "Practice evaluation" }, "PracticeSuccess")
  if compilation == nil then
    add_line(render, frame .. " Compiling submission", { section = "Practice evaluation" },
      "PracticeProgress")
  else
    add_line(render, (compilation and "✓ Compilation succeeded" or
      "✗ Compilation failed; continuing to review"), { section = "Practice evaluation" },
      compilation and "PracticeSuccess" or "PracticeWarning")
    if review_finished then
      add_line(render, "✓ Reviewer finished: " .. review_finished,
        { section = "Practice evaluation" }, "PracticeSuccess")
    elseif retry_delay then
      add_line(render, string.format("%s Reviewer retry %d of %d in %.1fs%s", frame,
        (attempt or 0) + 1, maximum_attempts, retry_delay,
        failure_category and " (" .. failure_category .. ")" or ""),
        { section = "Practice evaluation" }, "PracticeProgress")
    elseif attempt then
      add_line(render, string.format("%s Reviewer attempt %d of %d", frame, attempt,
        maximum_attempts), { section = "Practice evaluation" }, "PracticeProgress")
    else
      add_line(render, frame .. " Starting reviewer", { section = "Practice evaluation" },
        "PracticeProgress")
    end
  end
  blank(render)
  add_line(render, "Final feedback will replace this pane automatically.",
    { section = "Practice evaluation" }, "PracticeHint")
  set_feedback_lines(render)
end

function M.show_progress_error(error_message)
  local render = { lines = {}, contexts = {}, highlights = {}, positions = {} }
  add_line(render, "Practice evaluation failed", { section = "Evaluation error" },
    "PracticeFailure")
  blank(render)
  add_text(render, error_message, { section = "Evaluation error" })
  blank(render)
  add_line(render, "Return to the source, correct the problem, and submit again.",
    { section = "Evaluation error" }, "PracticeHint")
  set_feedback_lines(render)
end

function M.feedback_context(buffer, line)
  if not valid_buffer(feedback_buffer) or buffer ~= feedback_buffer then return nil end
  local context = feedback_contexts[line] or {}
  return { section = context.section, metadata_line = context.metadata_line,
    logical_section = context.logical_section }
end

return M
