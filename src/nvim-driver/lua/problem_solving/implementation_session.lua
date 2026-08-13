local process = require("practice.process")
local ui = require("problem_solving.ui")

local M = {}
local config, parent = nil, nil
local state = { draft = nil, source_buffer = nil, source_window = nil, pending = false, return_target = nil }

local function script(name) return config.scripts_dir .. "/" .. name end
local function valid(buffer) return buffer and vim.api.nvim_buf_is_valid(buffer) end
local function body(extra)
  return vim.tbl_extend("force", { collection_directory = state.return_target.collection, database_path = config.database_path }, extra or {})
end
local function source() return valid(state.source_buffer) and table.concat(vim.api.nvim_buf_get_lines(state.source_buffer, 0, -1, false), "\n") .. "\n" or state.draft.source end
local function save(callback)
  if not state.draft then return end
  process.run(config.python, script("problem_solving_implementation_draft.py"), body({ action = "save", draft_id = state.draft.draft_id, source = source() }), function(error, response)
    if not error and response.draft then state.draft = response.draft end
    if callback then callback(error, response) end
  end)
end
local function close()
  if valid(state.source_buffer) then vim.api.nvim_buf_delete(state.source_buffer, { force = true }) end
  state.source_buffer, state.source_window, state.draft = nil, nil, nil
end
local function open_source(draft)
  state.draft = draft
  vim.cmd("enew")
  state.source_window, state.source_buffer = vim.api.nvim_get_current_win(), vim.api.nvim_get_current_buf()
  vim.bo[state.source_buffer].buftype = "nofile"; vim.bo[state.source_buffer].bufhidden = "wipe"; vim.bo[state.source_buffer].swapfile = false; vim.bo[state.source_buffer].filetype = "cpp"
  vim.api.nvim_buf_set_name(state.source_buffer, "Level C implementation: " .. draft.problem_id .. ".cpp")
  vim.api.nvim_buf_set_lines(state.source_buffer, 0, -1, false, vim.split(draft.source, "\n", { plain = true }))
  vim.bo[state.source_buffer].modified = false
  vim.keymap.set("n", "<leader>c", M.compile, { buffer = state.source_buffer, silent = true, desc = "Problem solving: compile implementation" })
  vim.keymap.set("n", "<leader>k", M.check, { buffer = state.source_buffer, silent = true, desc = "Problem solving: check implementation" })
  vim.keymap.set("n", "<leader>f", M.finish, { buffer = state.source_buffer, silent = true, desc = "Problem solving: finish implementation" })
  vim.keymap.set("n", "<leader>q", M.return_to_card, { buffer = state.source_buffer, silent = true, desc = "Problem solving: return to card" })
  vim.api.nvim_create_autocmd("BufLeave", { buffer = state.source_buffer, callback = function() if state.draft then save() end end })
  ui.notify("Implementation workspace: <Space>c Compile · <Space>k Check · <Space>f Finish · <Space>q Return")
end

function M.setup(options, parent_session) config, parent = options, parent_session end
function M.active() return state.draft ~= nil end
function M.open_active()
  local current = parent.get_state()
  if current.status ~= "solving" and current.status ~= "revealed" and current.status ~= "discussing" then
    ui.notify("Implementation is available only for an active Level C card", vim.log.levels.WARN)
    return
  end
  M.open({ collection = current.collection, problem = current.problem })
end
function M.open(target)
  if state.draft then ui.notify("An implementation workspace is already open", vim.log.levels.WARN); return end
  state.return_target = target
  local function create(action)
    process.run(config.python, script("problem_solving_implementation_draft.py"), body({ action = action, problem_id = target.problem.id, language = config.implementation_language }), function(error, response)
      if error or type(response.draft) ~= "table" then ui.notify("Could not open draft: " .. tostring(error), vim.log.levels.ERROR); return end
      open_source(response.draft)
    end)
  end
  process.run(config.python, script("problem_solving_implementation_draft.py"), body({ action = "open", problem_id = target.problem.id, language = config.implementation_language }), function(error, response)
    if error or type(response.draft) ~= "table" then ui.notify("Could not load draft: " .. tostring(error), vim.log.levels.ERROR); return end
    if response.resumed then vim.ui.select({ "Resume", "Start fresh" }, { prompt = "Current implementation draft" }, function(choice) if choice == "Start fresh" then create("fresh") else open_source(response.draft) end end) else open_source(response.draft) end
  end)
end
function M.compile()
  if state.pending or not state.draft then return end
  state.pending = true
  save(function(error)
    if error then state.pending = false; ui.notify("Could not save draft: " .. error, vim.log.levels.ERROR); return end
    process.run(config.python, script("problem_solving_implementation_compile.py"), body({ draft_id = state.draft.draft_id, compiler = config.compiler }), function(compile_error, response)
      state.pending = false
      if compile_error then ui.notify("Compile request failed: " .. compile_error, vim.log.levels.ERROR); return end
      ui.open_implementation_feedback("Implementation compiler", response.diagnostics ~= "" and response.diagnostics or "Syntax check passed.")
      ui.notify(response.compiled and "Implementation compiled" or "Implementation has compiler diagnostics", response.compiled and vim.log.levels.INFO or vim.log.levels.WARN)
    end)
  end)
end
local function review(stage)
  if state.pending or not state.draft then return end
  state.pending = true
  save(function(error)
    if error then state.pending = false; ui.notify("Could not save draft: " .. error, vim.log.levels.ERROR); return end
    process.run(config.python, script("problem_solving_implementation_review.py"), body({ draft_id = state.draft.draft_id, stage = stage, reviewer = config.implementation_reviewer }), function(review_error, response)
      state.pending = false
      if review_error then ui.notify("Implementation review unavailable: " .. review_error, vim.log.levels.WARN); return end
      local text = response.feedback and vim.inspect(response.feedback) or "Reviewer unavailable. You can continue editing."
      ui.open_implementation_feedback("Implementation " .. stage .. " review", text)
    end)
  end)
end
function M.check() review("checkpoint") end
function M.finish() review("final") end
function M.return_to_card()
  if not state.draft then return end
  save(function() close(); parent.restore_after_implementation() end)
end
function M.drafts(collection)
  process.run(config.python, script("problem_solving_implementation_draft.py"), { collection_directory = collection, database_path = config.database_path, action = "list" }, function(error, response)
    if error or type(response.drafts) ~= "table" then ui.notify("Could not list drafts: " .. tostring(error), vim.log.levels.ERROR); return end
    ui.open_implementation_drafts(response.drafts, function(draft) M.open({ collection = collection, problem = { id = draft.problem_id } }) end)
  end)
end
function M.shutdown() if state.draft then save() end end
return M
