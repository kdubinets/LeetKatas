local problem_solving = require("problem_solving")

assert(vim.env.PROBLEM_SOLVING_DATABASE and vim.env.PROBLEM_SOLVING_DATABASE ~= "",
  "PROBLEM_SOLVING_DATABASE must point to a temporary test database")
assert(vim.o.termguicolors, "problem-solving mode must enable true-color support")
local which_key_directory = vim.fn.stdpath("data") .. "/leetkatas/which-key.nvim"
if vim.fn.isdirectory(which_key_directory) == 1 then
  assert(package.loaded["which-key"] ~= nil,
    "cached which-key.nvim was not loaded for problem-solving practice")
  assert(vim.o.runtimepath:find(which_key_directory, 1, true),
    "which-key.nvim was not added to the problem-solving runtime path")
end

local function wait_for(status)
  assert(vim.wait(10000, function()
    return problem_solving.get_state().status == status
  end, 10), "timed out waiting for problem-solving state " .. status)
end

local function wait_for_problem(problem_id, status)
  assert(vim.wait(10000, function()
    local state = problem_solving.get_state()
    return state.status == status and state.problem and state.problem.id == problem_id
  end, 10), "timed out waiting for problem " .. problem_id .. " in state " .. status)
end

local function buffer_text(buffer)
  return table.concat(vim.api.nvim_buf_get_lines(buffer, 0, -1, false), "\n")
end

local function find_buffer(variable)
  for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_valid(buffer) and vim.b[buffer][variable] then return buffer end
  end
end

for _, command in ipairs({
  "ProblemSolvingStart", "ProblemSolvingHint", "ProblemSolvingReveal",
  "ProblemSolvingBookmark", "ProblemSolvingBookmarks", "ProblemSolvingReopen",
  "ProblemSolvingUnbookmark", "ProblemSolvingNote", "ProblemSolvingRate",
  "ProblemSolvingAsk",
  "ProblemSolvingNext", "ProblemSolvingQuit", "ProblemSolvingStats",
  "ProblemSolvingSync", "ProblemSolvingDiagnostics",
}) do
  assert(vim.fn.exists(":" .. command) == 2, command .. " was not registered")
end
for _, mapping in ipairs({ "ps", "ph", "pr", "pg", "pb", "pl", "pm", "pc", "p1", "p2", "p3", "p4", "pn", "pt", "pq" }) do
  assert(vim.fn.maparg("<Space>" .. mapping, "n") ~= "", mapping .. " mapping is missing")
end

problem_solving.start()
wait_for("solving")
local state = problem_solving.get_state()
assert(state.problem.id == "problem-2", "canonical first problem was not selected")
assert(_G.ProblemSolvingStatusline and _G.ProblemSolvingStatusline():find("Add Two Numbers", 1, true),
  "problem-solving status line did not show the active problem")
assert(_G.ProblemSolvingStatusline():find("Solve 0:00", 1, true),
  "problem-solving status line did not show the active solve timer")
assert(vim.wait(10000, function()
  local line = _G.ProblemSolvingStatusline()
  return line:find("Today ", 1, true) and line:find("New solved ", 1, true)
    and line:find("New left ", 1, true) and line:find("Reviewed ", 1, true)
    and line:find("Due now ", 1, true) and line:find("Due later ", 1, true)
end, 10), "problem-solving status line did not show scheduling counters")
local brief = find_buffer("problem_solving_brief")
assert(brief and vim.bo[brief].readonly and not vim.bo[brief].modifiable,
  "problem brief is not read-only")
assert(buffer_text(brief):find("Add Two Numbers", 1, true), "problem brief was not rendered")
assert(not buffer_text(brief):find("Optional hint", 1, true), "hint leaked before request")
assert(not buffer_text(brief):find("Decisive insight", 1, true), "outline leaked before reveal")

problem_solving.ask("Which digit is at the head?")
assert(vim.wait(10000, function()
  local current = problem_solving.get_state()
  return not current.conversation_pending and #current.conversation_history == 2
end, 10), "clarification response did not complete")
assert(problem_solving.get_state().status == "solving",
  "clarification changed the solving state")
local conversation = find_buffer("problem_solving_conversation")
assert(conversation and buffer_text(conversation):find("least%-significant first"),
  "clarification was not rendered")

problem_solving.hint()
assert(vim.wait(10000, function()
  local current = find_buffer("problem_solving_brief")
  return current and buffer_text(current):find("Optional hint", 1, true)
end, 10), "optional hint was not rendered")

problem_solving.bookmark("Think about carry propagation")
wait_for("solving")
assert(problem_solving.get_state().problem.id == "problem-4",
  "bookmarked problem was not excluded from selection")

problem_solving.bookmarks()
assert(vim.wait(10000, function()
  for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_valid(buffer)
      and type(vim.b[buffer].problem_solving_bookmarks) == "table"
    then
      local bookmarks = vim.b[buffer].problem_solving_bookmarks
      return bookmarks[1] and bookmarks[1].note == "Think about carry propagation"
    end
  end
  return false
end, 10), "bookmark note was not retained")

problem_solving.reopen("problem-2")
wait_for_problem("problem-2", "solving")
assert(problem_solving.get_state().bookmarked, "reopened problem was not marked as bookmarked")
brief = find_buffer("problem_solving_brief")
assert(buffer_text(brief):find("Optional hint", 1, true), "reopened bookmark lost hint state")
assert(#problem_solving.get_state().conversation_history == 2,
  "reopened bookmark lost conversation history")

problem_solving.ask("Which algorithm should I use?")
assert(vim.wait(10000, function()
  local current = problem_solving.get_state()
  return not current.conversation_pending and #current.conversation_history == 4
end, 10), "clarification redirect did not complete")
conversation = find_buffer("problem_solving_conversation")
assert(buffer_text(conversation):find("would reveal solving guidance", 1, true),
  "clarification redirect was not rendered")

require("problem_solving.session").reveal(true)
wait_for("revealed")
assert(_G.ProblemSolvingStatusline():find("Outline revealed", 1, true),
  "problem-solving status line did not show the revealed outline")
local outline = find_buffer("problem_solving_outline")
assert(outline and vim.bo[outline].readonly and not vim.bo[outline].modifiable,
  "solution outline is not read-only")
assert(buffer_text(outline):find("Decisive insight", 1, true), "outline was not rendered")
assert(buffer_text(outline):find("after giving up", 1, true), "give-up state was not visible")

problem_solving.ask("Why is the invariant sufficient?")
assert(vim.wait(10000, function()
  local current = problem_solving.get_state()
  return not current.conversation_pending and current.status == "discussing"
    and #current.conversation_history == 6
end, 10), "post-reveal discussion did not complete")
conversation = find_buffer("problem_solving_conversation")
assert(buffer_text(conversation):find("invariant holds", 1, true),
  "post-reveal discussion was not rendered")

problem_solving.ask("UNAVAILABLE")
assert(vim.wait(10000, function()
  local current = problem_solving.get_state()
  return not current.conversation_pending and current.status == "discussing"
    and current.conversation_notice ~= nil
end, 10), "unavailable reviewer did not recover")
conversation = find_buffer("problem_solving_conversation")
assert(buffer_text(conversation):find("continue practicing", 1, true),
  "unavailable reviewer recovery was not rendered")

problem_solving.unbookmark()
assert(vim.wait(10000, function() return not problem_solving.get_state().bookmarked end, 10),
  "bookmark was not removed")
problem_solving.rate("good")
wait_for("solving")
assert(problem_solving.get_state().problem.id == "problem-4",
  "rating did not advance to the canonical next problem")

problem_solving.stats()
assert(vim.wait(10000, function()
  for _, buffer in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_valid(buffer) and vim.bo[buffer].filetype == "problem-solving-stats" then
      return buffer_text(buffer):find("Reviews: 1", 1, true) ~= nil
    end
  end
  return false
end, 10), "problem-solving statistics were not rendered")

problem_solving.next()
wait_for("solving")
assert(problem_solving.get_state().problem.id == "problem-8", "next did not advance selection")
problem_solving.quit()
assert(problem_solving.get_state().status == "idle", "quit did not reset the session")

local persisted_log = table.concat(vim.fn.readfile(vim.env.PROBLEM_SOLVING_LOG), "\n")
assert(not persisted_log:find("Which digit is at the head", 1, true),
  "conversation question leaked into the persistent log")
assert(not persisted_log:find("private adapter failure body", 1, true),
  "reviewer failure leaked into the persistent log")

vim.cmd("qa!")
