# 基于 Markdown + GitHub Pages

完全以 Markdown 文件的形式来书写和组织博客。**现在要做的只是写 Markdown**，以前的[这种方式](https://github.com/jackhai9/jackhai9.github.io)就有点复杂了。

## 项目说明

- **[这里](https://jackhai9.github.io/blog/)就是通过此方式创建的博客。**
- 仓库名可以任意起。
- 只有一个main分支，用于存放 Markdown 文件。当然可以使用其他分支。
- 手动开启这个仓库的 Github Pages 功能：Settings --> Pages --> 选择分支名并保存。

- GitHub Pages 会优先把仓库根目录的 index.html 或 index.md 作为首页，如果没有这两个，就会以 README.md 作为首页。

  > 如果根目录下没有 index.html 文件，GitHub Pages 使用默认的 [Jekyll](https://github.com/jekyll/jekyll) 这样的静态站点生成器，把 index.md 或者 README.md 这样的 Markdown 文件转成 HTML ，用于浏览器渲染和显示。截止目前2024年1月，Markdown 文件还不是浏览器原生支持渲染的格式。

## 整体流程

1. 手动 -- 克隆仓库
2. 手动 -- 本地写Markdown文件并自行控制文件之间的组织关系（链接引用、图片、目录等使用相对路径）
3. 手动 -- 提交Markdown文件到GitHub
4. 自动 -- Github Pages 会自动执行其内置的[workflow](https://github.com/jackhai9/blog/actions/workflows/pages/pages-build-deployment)最终部署到GitHub Pages
5. 附加功能：执行脚本`bash setup-hooks.sh`

## 概念说明

- [Markdown](https://daringfireball.net/projects/markdown/)：一种易写易读的标记语言，通过解析器转为 XHTML (or HTML)。语法因不同的解析器或编辑器而异。
- [GitHub Actions](https://docs.github.com/en/actions)：GitHub 提供的一种自动化工具，用于执行 workflow。
- [workflow](https://docs.github.com/en/actions/using-workflows/about-workflows)：工作流，即 按希望的顺序排列组合一系列指令（action）。这些指令可以是各种任务，如安装依赖、测试代码、部署应用等。
- [GitHub Pages](https://pages.github.com/)：GitHub 提供的一项服务，从 GitHub 仓库直接托管静态网站。常用于个人、项目或组织的网站，并且是免费的，不用再单独去申请域名，当然也支持指向你已申请的域名。很适合用来托管博客、项目文档、个人简历等。GitHub Pages 也默认使用 [Jekyll](https://github.com/jekyll/jekyll) 这样的静态站点生成器，直接把 Markdown 转成 HTML，见[我的另一个博客](https://github.com/jackhai9/blog)。在部署时会用到 GitHub Actions 提供的自动化构建和部署流程。总之，GitHub Pages为用户提供了一种简单便捷的方式，用于将代码和文档以网页的形式分享给他人。

## 其他说明

- **后续写博客只需要执行2、3就可以了。**

- Markdown编辑器：推荐Typora。

#### 配置SSH

通过SSH与GitHub进行免密交互，无需每次访问都使用用户名和密码，设置方式：

[检查本地现有的SSH密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)、[生成本地新的SSH密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)、[添加本地SSH密钥到GitHub账户](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)。

#### 添加favicon

默认是没有favicon的，如果需要添加：

1. 把你的favicon.ico放在根目录下，也就是跟index.md同一级目录。
2. 新建_includes/head-custom.html，内容如下：把其中的"blog"替换成你自己的仓库名

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="shortcut icon" type="image/x-icon" href="/blog/favicon.ico">
</head>
<body>
    
</body>
</html>
```





---

> 本文创建日期: 2024-01-28
>
> 最后更新日期: 2024-07-09