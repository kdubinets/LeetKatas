local practice = require("practice")

assert(vim.env.PRACTICE_DATABASE and vim.env.PRACTICE_DATABASE ~= "",
  "PRACTICE_DATABASE must point to a temporary test database")
assert(vim.env.PRACTICE_NOTES_DIRECTORY and vim.env.PRACTICE_NOTES_DIRECTORY ~= "",
  "PRACTICE_NOTES_DIRECTORY must point to a temporary test directory")

local function wait_for(status)
  local completed = vim.wait(10000, function()
    return practice.get_state().status == status
  end, 10)
  assert(completed, "timed out waiting for practice state " .. status)
end

local function buffer_text(buffer)
  return table.concat(vim.api.nvim_buf_get_lines(buffer, 0, -1, false), "\n")
end

local function buffer_starts_with(buffer, heading)
  local lines = vim.api.nvim_buf_get_lines(buffer, 0, 1, false)
  return lines[1] == heading
end

local function find_feedback_buffer()
  for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_valid(buffer) and vim.bo[buffer].filetype == "practice-feedback" then
      return buffer
    end
  end
end

local function press(keys)
  vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes(keys, true, false, true), "xt", false)
  vim.wait(100)
end

assert(vim.fn.exists(":PracticeStart") == 2, "PracticeStart was not registered")
assert(vim.fn.exists(":PracticeSubmit") == 2, "PracticeSubmit was not registered")
assert(vim.fn.exists(":PracticeAccept") == 2, "PracticeAccept was not registered")
assert(vim.fn.exists(":PracticeAsk") == 2, "PracticeAsk was not registered")
assert(vim.fn.exists(":PracticeRetry") == 2, "PracticeRetry was not registered")
assert(vim.fn.exists(":PracticeLog") == 2, "PracticeLog was not registered")
assert(vim.fn.exists(":PracticeDiagnostics") == 2, "PracticeDiagnostics was not registered")
assert(vim.fn.exists(":PracticeNote") == 2, "PracticeNote was not registered")
assert(vim.fn.exists(":PracticeNotes") == 2, "PracticeNotes was not registered")
assert(vim.fn.maparg("<Space>ps", "n") ~= "", "start mapping was not registered")
assert(vim.fn.maparg("<Space>pa", "n") ~= "", "accept mapping was not registered")
assert(vim.fn.maparg("<Space>pr", "n") ~= "", "retry mapping was not registered")
assert(vim.fn.maparg("<Space>pm", "n") ~= "", "note mapping was not registered")
assert(vim.fn.maparg("<Space>pf", "n") ~= "", "follow-up mapping was not registered")
assert(vim.fn.maparg("<Space>pm", "x") ~= "", "visual note mapping was not registered")
assert(vim.fn.maparg("<Space>po", "n") ~= "", "open notes mapping was not registered")
assert(vim.o.expandtab, "practice should indent with spaces")
assert(vim.o.shiftwidth == 4, "practice shiftwidth should be four")
assert(vim.o.softtabstop == 4, "practice softtabstop should be four")
assert(vim.o.tabstop == 4, "practice tabstop should be four")

local collection = vim.fn.tempname() .. "-practice-test"
assert(vim.fn.mkdir(collection, "p") == 1, "could not create test collection")
vim.fn.writefile({ vim.json.encode({
  language = { name = "C++", version = "C++20" },
  libraries = { { name = "C++ standard library", version = "C++20" } },
}) }, collection .. "/environment.json")
local function create_exercise(name)
  local source = collection .. "/" .. name .. ".cpp"
  vim.fn.writefile({
    "int solve() {",
    "    // Finish: return the answer",
    "}",
  }, source)
  vim.fn.writefile({
    "# Name",
    "",
    "Return Answer",
    "",
    "# Description",
    "",
    "Return the answer.",
    "",
    "# Solution",
    "",
    "```cpp",
    "return 42;",
    "```",
  }, collection .. "/" .. name .. ".md")
  return source
end

local original_sources = {
  answer = create_exercise("answer"),
  another_answer = create_exercise("another_answer"),
}

practice.start(collection)
wait_for("solving")

local first_state = practice.get_state()
assert(original_sources[first_state.exercise.id], "unexpected selected exercise")
local first_id = first_state.exercise.id
assert(first_state.working_path ~= original_sources[first_state.exercise.id],
  "original source was opened for editing")
assert(buffer_text(first_state.source_buffer):find("// Finish:", 1, true), "marker is missing")

vim.api.nvim_set_current_win(first_state.source_window)
vim.api.nvim_set_current_buf(first_state.source_buffer)
local solving_note = practice.note("research", 1, 2)
assert(solving_note and vim.api.nvim_buf_is_valid(solving_note), "solving note did not open")
vim.api.nvim_buf_set_lines(solving_note, -1, -1, false,
  { "Research whether this API has another useful form." })
vim.cmd("write")
local note_files = vim.fn.glob(vim.env.PRACTICE_NOTES_DIRECTORY .. "/*.md", false, true)
assert(#note_files == 1, "solving note was not saved")
assert(vim.fs.basename(note_files[1]):match("^%d%d%d%d%-%d%d%-%d%d%-%d%d%-%d%d%-%d%d%-%-"
  .. first_id .. "%.md$"), "practice note filename is not readable and exercise-specific")
local solving_note_text = table.concat(vim.fn.readfile(note_files[1]), "\n")
assert(solving_note_text:find("Kind: research", 1, true), "note kind is missing")
assert(solving_note_text:find("Phase: solving", 1, true), "solving phase is missing")
assert(solving_note_text:find(original_sources[first_id] .. ":1:", 1, true),
  "note does not point to the original source")
assert(not solving_note_text:find(first_state.working_path, 1, true),
  "note retained the temporary working path")
assert(solving_note_text:find("int solve()", 1, true)
  and solving_note_text:find("// Finish:", 1, true), "selected source context is missing")
vim.api.nvim_set_current_win(first_state.source_window)
vim.api.nvim_set_current_buf(first_state.source_buffer)

vim.api.nvim_buf_set_lines(first_state.source_buffer, 1, 2, false, { "    return 42;" })
practice.submit()
assert(practice.get_state().status == "evaluating", "submit did not enter evaluating state")
local progress_visible = false
for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
  if vim.api.nvim_buf_is_valid(buffer) and buffer_text(buffer):find("Practice evaluation", 1, true) then
    progress_visible = true
    break
  end
end
assert(progress_visible, "evaluation progress pane was not opened immediately")
wait_for("reviewing")

local review_state = practice.get_state()
assert(review_state.result.compiled == true, "completed source did not compile")
assert(review_state.result.proposed_rating == "good", "successful compile did not propose Good")
local successful_result = vim.deepcopy(review_state.result)

local feedback_buffer = find_feedback_buffer()
local feedback = feedback_buffer and buffer_text(feedback_buffer) or nil
assert(feedback, "feedback buffer was not opened")
assert(feedback:find("Correct  [Good]", 1, true), "outcome and rating are missing")
assert(feedback:find("The submitted implementation is correct.", 1, true),
  "structured reviewer feedback is missing")
assert(not feedback:find("return 42;", 1, true), "reference should be collapsed by default")
assert(feedback:find("Rating rationale", 1, true),
  "details should be expanded by default below Excellent")
assert(feedback:find("Detailed review  [d collapse]", 1, true),
  "expanded detailed review did not advertise its toggle")
assert(not feedback:find("Compiler details", 1, true), "empty diagnostics should be omitted")
assert(not feedback:find("**", 1, true) and not feedback:find("```", 1, true),
  "UI Markdown markers leaked into native feedback")
assert(feedback:find("Primary", 1, true) and feedback:find("Ratings", 1, true)
  and feedback:find("More", 1, true), "feedback actions are not grouped")
assert(not feedback:find("c Compiler", 1, true),
  "compiler shortcut was shown without compiler details")
assert(not feedback:find("t Chat", 1, true),
  "chat shortcut was shown before a follow-up conversation existed")
local colored_feedback = #vim.api.nvim_buf_get_extmarks(feedback_buffer, -1, 0, -1, {}) > 0
assert(colored_feedback, "feedback buffer did not receive color highlights")
vim.api.nvim_set_current_buf(feedback_buffer)
for _, key in ipairs({ "a", "1", "2", "3", "4", "n", "m", "d", "c", "r", "t", "?", "<CR>" }) do
  assert(vim.fn.maparg(key, "n", false, true).buffer == 1,
    "missing buffer-local feedback mapping: " .. key)
end
assert(not feedback:find("Shortcuts", 1, true), "redundant shortcut help is still displayed")

practice.ask("Why does this satisfy the exercise?")
local follow_up_completed = vim.wait(10000, function()
  local turns = practice.get_state().result.follow_up.turns
  return #turns == 1 and turns[1].status ~= "pending"
end, 10)
assert(follow_up_completed, "timed out waiting for follow-up response")
assert(practice.get_state().result.proposed_rating == "good",
  "follow-up chat changed the proposed rating")
feedback = buffer_text(feedback_buffer)
assert(feedback:find("Follow-up chat  [t collapse]", 1, true),
  "follow-up chat section was not opened")
assert(feedback:find("t Chat", 1, true),
  "chat shortcut was not shown after the conversation appeared")
assert(feedback:find("You", 1, true)
  and feedback:find("Why does this satisfy the exercise?", 1, true),
  "learner question is missing")
assert(feedback:find("The answer follows from the exercise requirement", 1, true),
  "reviewer answer is missing")
assert(feedback:find("gpt%-5%.6%-luna"), "follow-up model is missing")
assert(next(vim.api.nvim_get_hl(0, { name = "PracticeQuestion" })) ~= nil,
  "question highlight is missing")
assert(vim.api.nvim_get_hl(0, { name = "PracticeQuestionLabel" }).bold == true,
  "question header is not bold")
assert(vim.api.nvim_get_hl(0, { name = "PracticeAnswerLabel" }).bold == true,
  "answer header is not bold")
press("t")
feedback = buffer_text(feedback_buffer)
assert(feedback:find("Follow-up chat  [t expand]", 1, true)
  and not feedback:find("Why does this satisfy the exercise?", 1, true),
  "follow-up chat did not collapse")
press("t")
assert(buffer_text(feedback_buffer):find("Why does this satisfy the exercise?", 1, true),
  "follow-up chat did not re-expand")

press("d")
feedback = buffer_text(feedback_buffer)
assert(not feedback:find("Rating rationale", 1, true), "d did not collapse detailed review")
local cursor_line = vim.api.nvim_win_get_cursor(0)[1]
assert(vim.api.nvim_buf_get_lines(feedback_buffer, cursor_line - 1, cursor_line, false)[1]
  :find("Detailed review", 1, true), "detail toggle did not preserve section cursor")
press("d")
assert(buffer_text(feedback_buffer):find("Rating rationale", 1, true),
  "d did not re-expand detailed review")
press("r")
feedback = buffer_text(feedback_buffer)
assert(feedback:find("return 42;", 1, true), "r did not reveal the parsed reference")
assert(not feedback:find("# Solution", 1, true) and not feedback:find("```cpp", 1, true),
  "reference retained Markdown delimiters")
local reference_line = nil
for index, line in ipairs(vim.api.nvim_buf_get_lines(feedback_buffer, 0, -1, false)) do
  if line:find("return 42;", 1, true) then reference_line = index; break end
end
assert(reference_line, "reference code line was not found")
vim.api.nvim_win_set_cursor(0, { reference_line, 0 })
local review_note = practice.note("exercise-fix")
assert(review_note and vim.api.nvim_buf_is_valid(review_note), "review note did not open")
vim.api.nvim_buf_set_lines(review_note, -1, -1, false,
  { "Follow up on this reviewer observation." })
vim.cmd("write")
note_files = vim.fn.glob(vim.env.PRACTICE_NOTES_DIRECTORY .. "/*.md", false, true)
assert(#note_files == 2, "review note was not saved")
local review_note_text = nil
for _, path in ipairs(note_files) do
  local text = table.concat(vim.fn.readfile(path), "\n")
  if text:find("Phase: reviewing", 1, true) then
    review_note_text = text
    break
  end
end
assert(review_note_text, "review note phase is missing")
assert(review_note_text:find("Section: Exercise reference — Solution", 1, true),
  "review note section is missing")
assert(review_note_text:find(original_sources[first_id]:gsub("%.cpp$", ".md") .. ":12", 1, true),
  "review note did not retain exact metadata source line")
assert(review_note_text:find("return 42;", 1, true),
  "review note excerpt is missing")

local notes = require("practice.notes")
local collision_context = {
  filename_timestamp = "2000-01-02-03-04-05",
  created_at = "2000-01-02 03:04:05 +0000",
  collection = collection,
  exercise_id = "collision",
  phase = "solving",
  session_id = "test-session",
  context = original_sources[first_id] .. ":1:1",
  excerpt = "int solve()",
}
for _ = 1, 2 do
  local collision_note = notes.compose(collision_context, "follow-up")
  vim.api.nvim_buf_set_lines(collision_note, -1, -1, false, { "Keep this note." })
  vim.cmd("write")
end
assert(vim.fn.filereadable(vim.env.PRACTICE_NOTES_DIRECTORY
  .. "/2000-01-02-03-04-05--collision.md") == 1, "base collision note is missing")
assert(vim.fn.filereadable(vim.env.PRACTICE_NOTES_DIRECTORY
  .. "/2000-01-02-03-04-05--collision--2.md") == 1,
  "colliding note did not receive a numeric suffix")

local blank_context = vim.tbl_extend("force", collision_context, {
  filename_timestamp = "2000-01-02-03-04-06", exercise_id = "blank",
})
local blank_note = notes.compose(blank_context, "follow-up")
vim.cmd("write")
assert(vim.fn.glob(vim.env.PRACTICE_NOTES_DIRECTORY
  .. "/2000-01-02-03-04-06--blank*.md") == "", "blank note was saved")
vim.api.nvim_buf_delete(blank_note, { force = true })

local cancelled_context = vim.tbl_extend("force", collision_context, {
  filename_timestamp = "2000-01-02-03-04-07", exercise_id = "cancelled",
})
local cancelled_note = notes.compose(cancelled_context, "follow-up")
vim.api.nvim_buf_delete(cancelled_note, { force = true })
assert(vim.fn.glob(vim.env.PRACTICE_NOTES_DIRECTORY
  .. "/2000-01-02-03-04-07--cancelled*.md") == "", "cancelled note left a file")
vim.api.nvim_set_current_buf(feedback_buffer)
assert(table.concat(vim.fn.readfile(original_sources[first_state.exercise.id]), "\n")
  :find("// Finish:", 1, true),
  "original exercise was modified")

local first_submission = buffer_text(first_state.source_buffer)
practice.retry()
assert(practice.get_state().status == "solving", "retry did not return to solving")
assert(practice.get_state().previous_result ~= nil, "retry did not retain the previous result")
assert(buffer_text(first_state.source_buffer) == first_submission, "retry changed the working source")
assert(find_feedback_buffer() == nil, "retry did not close feedback")
practice.submit()
assert(practice.get_state().status == "evaluating", "retry submission did not enter evaluating")
assert(practice.get_state().previous_result == nil, "new submission retained the previous result")
wait_for("reviewing")
practice.accept()
wait_for("solving")
local second_state = practice.get_state()
assert(second_state.exercise.id ~= first_id, "unseen exercise was not selected next")
assert(buffer_text(second_state.source_buffer):find("// Finish:", 1, true),
  "new working copy did not start clean")

vim.api.nvim_buf_set_lines(second_state.source_buffer, 1, 2, false, { "    return;" })
practice.submit()
wait_for("reviewing")
feedback_buffer = find_feedback_buffer()
feedback = buffer_text(feedback_buffer)
assert(feedback:find("Almost there  [Acceptable]", 1, true),
  "minor defect outcome is missing")
assert(feedback:find("Correction", 1, true) and feedback:find("return 42;", 1, true),
  "reviewer correction was not expanded")
assert(feedback:find("recognized the approach", 1, true),
  "positive rating after failed compilation was not explained")
assert(feedback:find("Compiler details", 1, true), "non-empty diagnostics were omitted")
assert(feedback:find("c Compiler", 1, true),
  "compiler shortcut was not shown with compiler details")
for _, window in ipairs(vim.fn.win_findbuf(feedback_buffer)) do
  assert(vim.wo[window].wrap, "feedback window should wrap")
  assert(vim.wo[window].linebreak, "feedback wrapping should respect word boundaries")
  assert(vim.wo[window].breakindent, "wrapped feedback should preserve indentation")
end
vim.api.nvim_set_current_buf(feedback_buffer)
press("c")
assert(buffer_text(feedback_buffer):find("error:", 1, true),
  "c did not expand compiler diagnostics")
assert(not buffer_text(feedback_buffer):find("Shortcuts", 1, true),
  "shortcut help unexpectedly appeared")
press("<CR>")
assert(practice.get_state().status == "solving",
  "Enter on defective feedback did not return to editing")
assert(buffer_text(second_state.source_buffer):find("return;", 1, true),
  "defective-result retry changed the source")

vim.api.nvim_buf_set_lines(second_state.source_buffer, 1, 2, false, { "    return 0;" })
practice.submit()
wait_for("reviewing")
feedback_buffer = find_feedback_buffer()
feedback = buffer_text(feedback_buffer)
assert(feedback:find("Needs another attempt  [Fail]", 1, true),
  "incorrect outcome is missing")
practice.accept()
wait_for("complete")
local complete_state = practice.get_state()
assert(type(complete_state.next_due) == "string", "complete state did not include next due time")
assert(complete_state.exercise == nil, "complete state retained an exercise")

for _, source in pairs(original_sources) do
  assert(table.concat(vim.fn.readfile(source), "\n"):find("// Finish:", 1, true),
    "an original exercise was modified")
end

local archive_output = vim.fn.system({
  "python3", "-c",
  "import json,sqlite3,sys; c=sqlite3.connect(sys.argv[1]); "
    .. "rows=c.execute('SELECT submitted_source,review_response_json FROM review_artifacts ORDER BY review_id').fetchall(); "
    .. "print(json.dumps(rows))",
  vim.env.PRACTICE_DATABASE,
})
assert(vim.v.shell_error == 0, "could not inspect the review artifact archive")
local archived = vim.json.decode(archive_output)
assert(#archived == 2, "rated submissions were not archived")
assert(archived[1][1]:find("return 42;", 1, true), "successful submission source was not archived")
assert(archived[2][1]:find("return 0;", 1, true), "final incorrect submission was not archived")
assert(not archived[2][1]:find("return;", 1, true), "retried submission was archived")
assert(vim.json.decode(archived[1][2]).feedback.summary
  == "The submitted implementation is correct.", "full reviewer response was not archived")

local ui = require("practice.ui")
local excellent = vim.deepcopy(successful_result)
excellent.proposed_rating = "excellent"
local excellent_buffer = ui.open_feedback(vim.api.nvim_get_current_win(), excellent, {})
assert(buffer_text(excellent_buffer):find("Detailed review  [d expand]", 1, true),
  "Excellent feedback did not start with detailed review collapsed")
assert(not buffer_text(excellent_buffer):find("Rating rationale", 1, true),
  "Excellent feedback exposed detailed review by default")
ui.close_feedback()

local synthetic = {
  compiled = false,
  diagnostics = "",
  metadata = "# Legacy\n\n```cpp\nreturn 7;\n",
  metadata_sections = {},
  proposed_rating = vim.NIL,
  review = {
    status = "unavailable", failure = "**legacy** reviewer unavailable",
    reviewer = "legacy", attempts = 1,
  },
}
local old_columns = vim.o.columns
vim.o.columns = 160
local synthetic_buffer, synthetic_window = ui.open_feedback(vim.api.nvim_get_current_win(), synthetic, {})
assert(vim.api.nvim_win_get_width(synthetic_window) >= 52,
  "wide feedback did not keep the target minimum width")
local synthetic_text = buffer_text(synthetic_buffer)
assert(synthetic_text:find("Review unavailable", 1, true), "unavailable outcome is missing")
assert(synthetic_text:find("Choose a manual rating", 1, true), "manual-rating hint is missing")
vim.api.nvim_set_current_win(synthetic_window)
press("r")
synthetic_text = buffer_text(synthetic_buffer)
assert(synthetic_text:find("return 7;", 1, true), "malformed metadata fallback is missing")
assert(not synthetic_text:find("```", 1, true) and not synthetic_text:find("# Legacy", 1, true),
  "malformed metadata fallback retained Markdown delimiters")
ui.close_feedback()

vim.o.columns = 100
synthetic_buffer, synthetic_window = ui.open_feedback(vim.api.nvim_get_current_win(), synthetic, {})
assert(vim.api.nvim_win_get_height(synthetic_window) >= 10,
  "narrow feedback did not receive a usable horizontal height")
ui.close_feedback()
vim.o.columns = old_columns

practice.quit()
assert(practice.get_state().status == "idle", "practice did not return to idle")
practice.open_notes()
assert(vim.fn.isdirectory(vim.env.PRACTICE_NOTES_DIRECTORY) == 1,
  "PracticeNotes did not target the configured notes directory")
assert(vim.env.PRACTICE_LOG and vim.fn.filereadable(vim.env.PRACTICE_LOG) == 1,
  "persistent practice log was not created")
local log_text = table.concat(vim.fn.readfile(vim.env.PRACTICE_LOG), "\n")
local directory_opened = vim.fn.fnamemodify(vim.api.nvim_buf_get_name(0), ":p")
  == vim.fn.fnamemodify(vim.env.PRACTICE_NOTES_DIRECTORY, ":p")
assert(directory_opened or log_text:find("Practice notes: "
  .. vim.env.PRACTICE_NOTES_DIRECTORY, 1, true),
  "PracticeNotes neither opened nor reported the configured directory")
assert(log_text:find("process_started", 1, true), "process start was not logged")
assert(log_text:find("process_finished", 1, true), "process result was not logged")
vim.fn.delete(collection, "rf")

print("Neovim practice headless workflow passed")
