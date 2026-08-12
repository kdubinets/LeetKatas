local M = {}

local function popup_key(key, fallback)
  return function()
    return vim.fn.pumvisible() == 1 and key or fallback
  end
end

function M.enable(buffer)
  -- Limit keyword completion to the active exercise buffer.  This keeps
  -- suggestions local and avoids exposing words from notes or other buffers.
  vim.bo[buffer].complete = "."
  -- With no `noselect`, Neovim highlights the first suggestion immediately.
  vim.bo[buffer].completeopt = "menuone"

  vim.keymap.set("i", "<C-Space>", "<C-x><C-n>", {
    buffer = buffer,
    silent = true,
    desc = "Practice: complete from the current exercise",
  })
  vim.keymap.set("i", "<Up>", popup_key("<C-p>", "<Up>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: previous completion",
  })
  vim.keymap.set("i", "<Down>", popup_key("<C-n>", "<Down>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: next completion",
  })
  vim.keymap.set("i", "<C-k>", popup_key("<C-p>", "<C-k>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: previous completion",
  })
  vim.keymap.set("i", "<C-j>", popup_key("<C-n>", "<C-j>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: next completion",
  })
  vim.keymap.set("i", "<Tab>", popup_key("<C-n>", "<Tab>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: next completion",
  })
  vim.keymap.set("i", "<S-Tab>", popup_key("<C-p>", "<S-Tab>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: previous completion",
  })
  vim.keymap.set("i", "<C-[>", popup_key("<C-e>", "<C-[>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: dismiss completion",
  })
  vim.keymap.set("i", "<CR>", popup_key("<C-y>", "<CR>"), {
    buffer = buffer,
    expr = true,
    silent = true,
    desc = "Practice: accept completion",
  })
end

return M
