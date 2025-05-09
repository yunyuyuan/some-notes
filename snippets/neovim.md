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
-- <leader>+l = console.log
vim.api.nvim_set_keymap('x', '<leader>l', 'y<ESC>o<ESC>iconsole.log(\'<C-r>":\', <C-r>")<ESC>', { noremap = true, silent = true })
vim.opt.clipboard = "unnamedplus"


require("lazy").setup({
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
  {
    "gennaro-tedesco/nvim-peekup",
  },
  {
    "keaising/im-select.nvim",
    config = function()
        require("im_select").setup({
          set_previous_events = {},
        })
    end,
  },
  {
    "max397574/better-escape.nvim",
    config = function()
      require("better_escape").setup()
    end,
  }
})
```