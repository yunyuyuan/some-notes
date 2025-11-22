import { defineConfig, DefaultTheme } from 'vitepress';
import fs from 'fs';
import path from 'path';

function getSidebar() {
  const result: DefaultTheme.Sidebar = [];
  let md = '';
  const config = JSON.parse(fs.readFileSync(path.resolve(__dirname, "../config.json")).toString());
  config.forEach(item => {
    let s = `* **${item.dir}**: ${item.description}\n`;
    result.push({
      text: item.title,
      collapsed: true,
      items: item.children.map(i => {
        s += `  * [${i.name}](/${item.dir}/${i.file})：${i.description}\n`;
        return {
          text: i.name,
          link: `/${item.dir}/${i.file}`
        }
      })
    })
    md += s;
  })
  fs.writeFileSync(path.resolve(__dirname, "../list.md"), md);
  return result;
}

// https://vitepress.vuejs.org/reference/site-config
export default defineConfig({
  title: "Some Notes",
  description: "A VitePress Site",
  themeConfig: {
    // https://vitepress.vuejs.org/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Edit', link: 'https://code-server-cf.yunyuyuan.net/?folder=/opt/code/some-notes' },
    ],

    algolia: {
      appId: 'UX7BHMEFLB',
      apiKey: 'b2813fef888fb39b177d35d0c444921e',
      indexName: 'some-yunyuyuan'
    },

    sidebar: getSidebar(),

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yunyuyuan/some-notes' }
    ]
  }
})
