import { defineConfig } from 'vitepress'

// https://vitepress.vuejs.org/reference/site-config
export default defineConfig({
  title: "self-host-starter",
  description: "A VitePress Site",
  themeConfig: {
    // https://vitepress.vuejs.org/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
    ],

    sidebar: [
      {
        text: 'Linux 服务器相关',
        link: '/linux-server/README.md',
        collapsed: true,
        items: [
          { text: 'acme.sh', link: '/linux-server/acme' },
          { text: 'aria2', link: '/linux-server/aria2' },
          { text: 'backup', link: '/linux-server/backup' },
          { text: 'cf-tunnel', link: '/linux-server/cloudflare-tunnel' },
          { text: 'ddns-cf', link: '/linux-server/ddns-cf' },
          { text: 'interface', link: '/linux-server/interface' },
          { text: 'netdata', link: '/linux-server/netdata' },
          { text: 'nginx', link: '/linux-server/nginx' },
          { text: 'openwrt', link: '/linux-server/openwrt' },
        ]
      },
      {
        text: 'Angular相关',
        link: '/angular/README.md',
        collapsed: true,
        items: [
        ]
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yunyuyuan/self-host-starter' }
    ]
  }
})
