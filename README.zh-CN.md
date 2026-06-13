# Markdown Blog

<p align="center">
  简体中文 | <a href="README.md">English</a>
</p>

这个仓库是一个基于 Markdown 和 GitHub Pages 的个人博客。主要流程保持简单：写 Markdown，提交到 `main`，由 GitHub Pages 渲染并发布站点。

线上站点：[jackhai9.github.io/blog](https://jackhai9.github.io/blog/)

## 仓库用途

- 用普通 Markdown 文件保存博客文章。
- 直接通过 GitHub Pages 发布仓库内容。
- 避免旧版 `jackhai9.github.io` 仓库里较重的 Hexo 工作流。
- 让图片、链接和文章结构尽量贴近源文件。

## 仓库结构

- `index.md` 是博客入口页。
- `src/` 存放文章 Markdown 文件。
- `_config.yml` 配置 GitHub Pages/Jekyll 站点元数据。
- `_layouts/default.html` 覆盖默认 Primer 布局，并移除由许可证触发的默认页脚。
- `_includes/head-custom.html` 自定义生成页面的 HTML head。
- `scripts/` 存放文章元数据和迁移相关的本地维护脚本。
- `hooks/` 存放由 `scripts/setup-hooks.sh` 安装的 Git hook 模板。

## 写作流程

1. 在 `src/` 下创建或编辑 Markdown 文件。
2. 本地文章和图片使用相对链接。
3. 把 Markdown 变更提交到 `main`。
4. GitHub Pages 构建并发布站点。

可选的本地 hook 安装：

```bash
bash scripts/setup-hooks.sh
```

这个 hook 会在提交前更新文章的创建日期和最后更新日期。

## 旧博客

旧版 Hexo 博客位于 [`jackhai9/jackhai9.github.io`](https://github.com/jackhai9/jackhai9.github.io)。

## License

除非另有说明，文字内容使用 Creative Commons Attribution 4.0 International 许可。本地自动化脚本按 [LICENSE](LICENSE) 中描述的 MIT 条款提供。
