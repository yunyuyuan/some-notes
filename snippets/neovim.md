# Neovim configuration

```sh
vim ~/.config/nvim/init.lua
```
```lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)
vim.g.mapleader = ","

vim.api.nvim_set_keymap('n', '<leader>m', '<cmd>lua require"hop".hint_words()<CR>', { silent = true })
vim.api.nvim_set_keymap('i', 'jj', '<Esc>', { noremap = true, silent = true })
vim.opt.clipboard = "unnamedplus"

require("lazy").setup({
  {
    "yunyuyuan/vim-barbaric",
    init = function()
      vim.g.barbaric_switchback = 1
    end,
  },
  {
    "phaazon/hop.nvim",
    config = function ()
        require("hop").setup()
    end,
  },
  {
    "tpope/vim-surround",
  },
  {
    "matze/vim-move",
    init = function()
      vim.g.move_key_modifier_visualmode = 'S'
    end,
  },
  {
    "tpope/vim-repeat",
  },
})

```