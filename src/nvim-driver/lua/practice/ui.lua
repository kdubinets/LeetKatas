local M = {}
local log = require("practice.log")
local import_folds = require("practice.import_folds")

local feedback_buffer = nil
local feedback_window = nil
local feedback_namespace = vim.api.nvim_create_namespace("practice_feedback")
local instruction_namespace = vim.api.nvim_create_namespace("practice_instruction")
local feedback_contexts = {}
local feedback_result = nil
local feedback_callbacks = nil
local expanded = { review = false, compiler = false, reference = false, chat = true }
local review_started_collapsed = false
local stats_buffer = nil
local stats_window = nil

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
end

define_highlights()

local function valid_buffer(buffer)
  return buffer ~= nil and vim.api.nvim_buf_is_valid(buffer)
end

local function valid_window(window)
  return window ~= nil and vim.api.nvim_win_is_valid(window)
end

local function title_case(value)
  return value:sub(1, 1):upper() .. value:sub(2)
end

local function format_duration(milliseconds, tracked, total)
  if total > 0 and tracked == 0 then return "untracked" end
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

local function stats_lines(stats)
  local today, collection, forecast = stats.today, stats.collection_state, stats.forecast
  local lines = {
    "Practice statistics",
    vim.fs.basename(stats.collection) .. "  " .. stats.collection,
    "",
    "Today  " .. today.date,
    string.format("  Completed             %d", today.reviews),
    string.format("  Due now               %d", today.due_now),
    string.format("  Due later today       %d", today.due_later_today),
    string.format("  New introduced        %d", today.new_introduced),
    string.format("  Practice time         %s",
      format_duration(today.practice_time_ms, today.tracked_reviews, today.reviews)),
    string.format("  Ratings               Fail %d · Acceptable %d · Good %d · Excellent %d",
      today.ratings.fail, today.ratings.acceptable, today.ratings.good,
      today.ratings.excellent),
    "",
    "Collection",
    string.format("  Total                 %d", collection.total),
    string.format("  Unseen                %d", collection.unseen),
    string.format("  Introduced            %d", collection.introduced),
    string.format("  Learning              %d", collection.learning),
    string.format("  Learned (FSRS Review) %d", collection.learned),
    string.format("  Relearning            %d", collection.relearning),
    "",
    "Forecast",
    string.format("  Scheduled tomorrow    %d", forecast.tomorrow_due),
  }
  for _, day in ipairs(forecast.days) do
    table.insert(lines, string.format("  %s             %d", day.date, day.due))
  end
  vim.list_extend(lines, {
    "",
    "Recent history",
    "  Date         Reviews  New  F  A  G  E  Time",
  })
  for _, day in ipairs(stats.history) do
    table.insert(lines, string.format("  %s  %7d  %3d  %d  %d  %d  %d  %s",
      day.date, day.reviews, day.new_introduced, day.ratings.fail,
      day.ratings.acceptable, day.ratings.good, day.ratings.excellent,
      format_duration(day.practice_time_ms, day.tracked_reviews, day.reviews)))
  end
  table.insert(lines, "")
  table.insert(lines, "r Refresh   q Close")
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
    add_line(render, "Structured review is unavailable. Choose a manual rating.",
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
    add_line(render, "Primary   a / <Space>pa  Accept " .. rating .. " and continue",
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
  if review_started_collapsed and review then
    if type(review.version_notes) == "string" and review.version_notes ~= "" then
      table.insert(details, "Version notes in review")
    end
    if type(review.improved_implementation) == "string" and review.improved_implementation ~= "" then
      table.insert(details, "Improved implementation in review")
    end
  end
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

function M.confirm_discard(action)
  return vim.fn.confirm("The current attempt has unsaved changes. Discard them and " .. action .. "?",
    "&Discard\n&Cancel", 2) == 1
end

function M.close_feedback()
  if valid_window(feedback_window) then vim.api.nvim_win_close(feedback_window, true) end
  if valid_buffer(feedback_buffer) then vim.api.nvim_buf_delete(feedback_buffer, { force = true }) end
  feedback_window, feedback_buffer = nil, nil
  feedback_contexts, feedback_result, feedback_callbacks = {}, nil, nil
  expanded = { review = false, compiler = false, reference = false, chat = true }
  review_started_collapsed = false
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
  vim.api.nvim_buf_set_lines(stats_buffer, 0, -1, false, stats_lines(stats))
  vim.api.nvim_buf_clear_namespace(stats_buffer, feedback_namespace, 0, -1)
  for _, line in ipairs({ 0, 3, 11, 19, 29 }) do
    vim.api.nvim_buf_add_highlight(stats_buffer, feedback_namespace, "PracticeHeading", line, 0, -1)
  end
  vim.api.nvim_buf_add_highlight(stats_buffer, feedback_namespace, "PracticeHint",
    vim.api.nvim_buf_line_count(stats_buffer) - 1, 0, -1)
  vim.bo[stats_buffer].modifiable = false
  vim.bo[stats_buffer].readonly = true
  vim.api.nvim_set_current_win(stats_window)
  return stats_buffer, stats_window
end

function M.open_source(path, preferred_window, practice_marker)
  M.close_feedback()
  if valid_window(preferred_window) then vim.api.nvim_set_current_win(preferred_window) end
  vim.cmd("edit! " .. vim.fn.fnameescape(path))
  local buffer, window = vim.api.nvim_get_current_buf(), vim.api.nvim_get_current_win()
  vim.bo[buffer].bufhidden = "wipe"
  vim.bo[buffer].swapfile = false
  vim.bo[buffer].completefunc, vim.bo[buffer].omnifunc, vim.bo[buffer].tagfunc = "", "", ""
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
  expanded.review = result.proposed_rating ~= "excellent"
  review_started_collapsed = not expanded.review
  local render = render_feedback("outcome")
  local _, _, review = outcome(result)
  local has_improved_implementation = review ~= nil
    and type(review.improved_implementation) == "string"
    and review.improved_implementation ~= ""
  local has_version_notes = review ~= nil
    and type(review.version_notes) == "string"
    and review.version_notes ~= ""
  local rendered_improved_hint, rendered_version_hint = false, false
  for _, line in ipairs(render and render.lines or {}) do
    if line:find("Improved implementation in review", 1, true) then
      rendered_improved_hint = true
    end
    if line:find("Version notes in review", 1, true) then
      rendered_version_hint = true
    end
  end
  local buffer_improved_hint, buffer_version_hint = false, false
  if valid_buffer(feedback_buffer) then
    for _, line in ipairs(vim.api.nvim_buf_get_lines(feedback_buffer, 0, -1, false)) do
      if line:find("Improved implementation in review", 1, true) then
        buffer_improved_hint = true
      end
      if line:find("Version notes in review", 1, true) then
        buffer_version_hint = true
      end
    end
  end
  log.event("feedback_opened", "info", {
    proposed_rating = type(result.proposed_rating) == "string" and result.proposed_rating or nil,
    review_status = type(result.review) == "table" and result.review.status or nil,
    review_verdict = review and review.verdict or nil,
    review_started_collapsed = review_started_collapsed,
    has_improved_implementation = has_improved_implementation,
    has_version_notes = has_version_notes,
    rendered_improved_hint = rendered_improved_hint,
    rendered_version_hint = rendered_version_hint,
    buffer_improved_hint = buffer_improved_hint,
    buffer_version_hint = buffer_version_hint,
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
  local compilation, attempt, retry_delay, review_finished = nil, nil, nil, nil
  local maximum_attempts = 3
  for _, event in ipairs(events) do
    if event.event == "compilation_finished" then compilation = event.compiled
    elseif event.event == "review_attempt_started" then
      attempt, maximum_attempts, retry_delay = event.attempt,
        event.maximum_attempts or maximum_attempts, nil
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
      add_line(render, string.format("%s Reviewer retry %d of %d in %.1fs", frame,
        (attempt or 0) + 1, maximum_attempts, retry_delay),
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
