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

assert(vim.fn.exists(":PracticeStart") == 2, "PracticeStart was not registered")
assert(vim.fn.exists(":PracticeSubmit") == 2, "PracticeSubmit was not registered")
assert(vim.fn.exists(":PracticeAccept") == 2, "PracticeAccept was not registered")
assert(vim.fn.exists(":PracticeLog") == 2, "PracticeLog was not registered")
assert(vim.fn.exists(":PracticeDiagnostics") == 2, "PracticeDiagnostics was not registered")
assert(vim.fn.exists(":PracticeNote") == 2, "PracticeNote was not registered")
assert(vim.fn.exists(":PracticeNotes") == 2, "PracticeNotes was not registered")
assert(vim.fn.maparg("<Space>ps", "n") ~= "", "start mapping was not registered")
assert(vim.fn.maparg("<Space>pa", "n") ~= "", "accept mapping was not registered")
assert(vim.fn.maparg("<Space>pm", "n") ~= "", "note mapping was not registered")
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
  if vim.api.nvim_buf_is_valid(buffer) and buffer_text(buffer):find("# Practice Evaluation", 1, true) then
    progress_visible = true
    break
  end
end
assert(progress_visible, "evaluation progress pane was not opened immediately")
wait_for("reviewing")

local review_state = practice.get_state()
assert(review_state.result.compiled == true, "completed source did not compile")
assert(review_state.result.proposed_rating == "good", "successful compile did not propose Good")

local feedback = nil
for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
  if vim.api.nvim_buf_is_valid(buffer) and vim.bo[buffer].filetype == "markdown" then
    local text = buffer_text(buffer)
    if buffer_starts_with(buffer, "# Practice Feedback") then
      feedback = text
      break
    end
  end
end
assert(feedback, "feedback buffer was not opened")
assert(feedback:find("Compilation:** SUCCESS", 1, true), "compile result is missing")
assert(feedback:find("return 42;", 1, true), "reference solution is missing")
assert(feedback:find("The submitted implementation is correct.", 1, true),
  "structured reviewer feedback is missing")
assert(feedback:find("Rating rationale", 1, true), "review rating rationale is missing")
local colored_feedback = false
for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
  if vim.api.nvim_buf_is_valid(buffer) and buffer_starts_with(buffer, "# Practice Feedback") then
    colored_feedback = #vim.api.nvim_buf_get_extmarks(buffer, -1, 0, -1, {}) > 0
    break
  end
end
assert(colored_feedback, "feedback buffer did not receive color highlights")
local feedback_buffer = vim.api.nvim_get_current_buf()
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
assert(review_note_text:find("Section: # Practice Feedback", 1, true),
  "review note section is missing")
assert(review_note_text:find("# Practice Feedback", 1, true),
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

practice.accept()
wait_for("solving")
local second_state = practice.get_state()
assert(second_state.exercise.id ~= first_id, "unseen exercise was not selected next")
assert(buffer_text(second_state.source_buffer):find("// Finish:", 1, true),
  "new working copy did not start clean")

vim.api.nvim_buf_set_lines(second_state.source_buffer, 1, 2, false, { "    return;" })
practice.submit()
wait_for("reviewing")
local correction_visible = false
for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
  if vim.api.nvim_buf_is_valid(buffer) then
    local text = buffer_text(buffer)
    if buffer_starts_with(buffer, "# Practice Feedback") then
      correction_visible = text:find("## Corrected implementation", 1, true) ~= nil
        and text:find("return 42;", 1, true) ~= nil
      for _, window in ipairs(vim.fn.win_findbuf(buffer)) do
        assert(vim.wo[window].wrap, "feedback window should wrap")
        assert(vim.wo[window].linebreak, "feedback wrapping should respect word boundaries")
        assert(vim.wo[window].breakindent, "wrapped feedback should preserve indentation")
      end
      break
    end
  end
end
assert(correction_visible, "reviewer correction was not rendered")
practice.accept()
wait_for("complete")
local complete_state = practice.get_state()
assert(type(complete_state.next_due) == "string", "complete state did not include next due time")
assert(complete_state.exercise == nil, "complete state retained an exercise")

for _, source in pairs(original_sources) do
  assert(table.concat(vim.fn.readfile(source), "\n"):find("// Finish:", 1, true),
    "an original exercise was modified")
end

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
