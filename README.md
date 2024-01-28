# blog

完全以 Markdown 文件的形式来书写和组织博客。**要做的只是写 Markdown**，相较而言[这个](https://github.com/jackhai9/jackhai9.github.io/tree/source)就有点复杂了。

## 项目说明

- 仓库名可以任意起。
- 只有一个main分支，存放 Markdown 文件。当然可以创建其他分支。
- 手动开启 Github Pages 功能：Settings --> Pages --> 选择分支名并保存。

- GitHub Pages 会优先把 index.html 或 index.md 作为首页，如果没有这两个，就会以 README.md 作为首页。

## 整体流程

1. 手动 -- 克隆仓库
2. 手动 -- 本地写Markdown文件并自行控制文件之间的组织关系（链接引用、图片、目录等使用相对路径）

 

如果根目录下没有 index.html 文件，GitHub Pages 默认使用 [Jekyll](https://github.com/jekyll/jekyll) 这样的静态站点生成器，会把 index.md 或者 README.md 这样的 Markdown 文件转成 HTML ，用于浏览器解析和显示。截止目前2024年1月，Markdown 文件还不是浏览器原生支持的格式。
