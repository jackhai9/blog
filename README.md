# blog

完全以 Markdown 文件的形式来书写和组织博客。**要做的只是写 Markdown**，相较而言[这个](https://github.com/jackhai9/jackhai9.github.io/tree/source)就有点复杂了。

## 项目说明

- 仓库名可以任意起。
- 只有一个main分支，存放 Markdown 文件。当然可以使用其他分支。
- 手动开启这个仓库的 Github Pages 功能：Settings --> Pages --> 选择分支名并保存。

- GitHub Pages 会优先把仓库根目录的 index.html 或 index.md 作为首页，如果没有这两个，就会以 README.md 作为首页。

## 整体流程

1. 手动 -- 克隆仓库
2. 手动 -- 本地写Markdown文件并自行控制文件之间的组织关系（链接引用、图片、目录等使用相对路径）
3. 手动 -- 提交Markdown文件到GitHub
4. 自动 -- Github Pages 会自动执行[workflow](https://github.com/jackhai9/blog/actions/workflows/pages/pages-build-deployment)最终部署到GitHub Pages

 

如果根目录下没有 index.html 文件，GitHub Pages 默认使用 [Jekyll](https://github.com/jekyll/jekyll) 这样的静态站点生成器，把 index.md 或者 README.md 这样的 Markdown 文件转成 HTML ，用于浏览器解析和显示。截止目前2024年1月，Markdown 文件还不是浏览器原生支持渲染的格式。
