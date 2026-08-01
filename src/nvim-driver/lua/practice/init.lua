local session = require("practice.session")

local M = {}

local RATINGS = { "fail", "acceptable", "good", "excellent" }

local function map(lhs, rhs, description)
  vim.keymap.set("n", lhs, rhs, { silent = true, desc = description })
end

function M.setup(options)
  session.setup(options)

  vim.api.nvim_create_user_command("PracticeStart", function(command)
    session.start(command.args ~= "" and command.args or nil)
  end, { nargs = "?", complete = "dir", desc = "Start a coding practice session" })

  vim.api.nvim_create_user_command("PracticeSubmit", session.submit, {
    desc = "Submit the current practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeAccept", session.accept, {
    desc = "Accept the proposed practice rating",
  })
  vim.api.nvim_create_user_command("PracticeRate", function(command)
    session.rate(command.args)
  end, {
    nargs = 1,
    complete = function(argument_lead)
      return vim.tbl_filter(function(rating)
        return vim.startswith(rating, argument_lead:lower())
      end, RATINGS)
    end,
    desc = "Override the proposed practice rating",
  })
  vim.api.nvim_create_user_command("PracticeNext", session.next, {
    desc = "Skip to the next practice exercise",
  })
  vim.api.nvim_create_user_command("PracticeQuit", session.quit, {
    desc = "End the coding practice session",
  })

  map("<leader>ps", M.start, "Practice: start")
  map("<leader>pc", M.submit, "Practice: check current solution")
  map("<leader>pa", M.accept, "Practice: accept proposed rating")
  map("<leader>p1", function() M.rate("fail") end, "Practice: rate Fail")
  map("<leader>p2", function() M.rate("acceptable") end, "Practice: rate Acceptable")
  map("<leader>p3", function() M.rate("good") end, "Practice: rate Good")
  map("<leader>p4", function() M.rate("excellent") end, "Practice: rate Excellent")
  map("<leader>pn", M.next, "Practice: next exercise")
  map("<leader>pq", M.quit, "Practice: quit")
end

function M.start(directory)
  session.start(directory)
end

function M.submit()
  session.submit()
end

function M.accept()
  session.accept()
end

function M.rate(rating)
  session.rate(rating)
end

function M.next()
  session.next()
end

function M.quit()
  session.quit()
end

function M.get_state()
  return session.get_state()
end

return M
