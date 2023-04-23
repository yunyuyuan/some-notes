import { defineConfig } from 'vitepress'

// https://vitepress.vuejs.org/reference/site-config
export default defineConfig({
  title: "Some Notes",
  description: "A VitePress Site",
  themeConfig: {
    // https://vitepress.vuejs.org/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Edit', link: 'https://code-server-cf.yunyuyuan.net/?folder=/opt/codes/some-notes' },
    ],

    algolia: {
      appId: 'UX7BHMEFLB',
      apiKey: 'b2813fef888fb39b177d35d0c444921e',
      indexName: 'some-yunyuyuan'
    },

    sidebar: [
      {
        text: 'Linux 服务器相关',
        collapsed: true,
        items: [
          { text: 'acme.sh', link: '/linux-server/acme' },
          { text: 'aria2', link: '/linux-server/aria2' },
          { text: 'backup', link: '/linux-server/backup' },
          { text: 'cf-tunnel', link: '/linux-server/cloudflare-tunnel' },
          { text: 'code-serevr', link: '/linux-server/code-server' },
          { text: 'ddns-cf', link: '/linux-server/ddns-cf' },
          { text: 'interface', link: '/linux-server/interface' },
          { text: 'netdata', link: '/linux-server/netdata' },
          { text: 'nginx', link: '/linux-server/nginx' },
          { text: 'openwrt', link: '/linux-server/openwrt' },
        ]
      },
      {
        text: '前端',
        collapsed: true,
        items: [
          { text: 'vertical-center', link: '/front-end/vertical-center' },
          { text: 'dark-mode', link: '/front-end/dark-mode' },
          { text: 'diagonal', link: '/front-end/diagonal' },
        ]
      },
      {
        text: '脚本',
        collapsed: true,
        items: [
          { text: 'batch-rename', link: '/scripts/batch-rename' },
        ]
      },
      {
        text: '速记',
        collapsed: true,
        items: [
          { text: 'git-multiple-user', link: '/snippets/git-domain-map-user' },
          { text: 'neovim', link: '/snippets/neovim' },
        ]
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yunyuyuan/some-notes' }
    ]
  }
})
