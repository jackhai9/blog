# 项目补充说明

这份文档补充说明这个博客仓库的设计取舍、发布方式和常见配置。主 README 保持简洁，这里保留更偏背景和操作细节的内容。

## 项目定位

这个仓库是一个尽量简单的 Markdown 博客：

- 文章直接写成 Markdown 文件。
- 首页使用根目录的 `index.md`。
- 文章和归档内容主要放在 `src/`。
- 图片、文章链接和目录结构尽量贴近源文件。
- 不维护复杂博客框架，避免把写作流程变重。

日常写作通常只需要编辑 Markdown、提交变更，然后让 GitHub Pages 自动发布。

## 仓库结构补充

当前主要文件和目录的作用：

- `index.md`：博客首页入口。
- `src/`：文章 Markdown 文件。
- `src/legacy/`：从旧博客迁移过来的历史文章。
- `src/image/`：本仓库内保存的图片资源。
- `_config.yml`：Jekyll/GitHub Pages 站点元数据，例如标题、描述、语言。
- `_includes/head-custom.html`：注入 favicon、夜间模式样式和脚本。
- `_layouts/default.html`：覆盖默认 Primer layout，保留主体结构，同时移除许可证触发的默认页脚。
- `scripts/`：本地维护脚本，包括文章日期处理和旧博客迁移辅助脚本。
- `hooks/`：Git hook 模板，配合 `scripts/setup-hooks.sh` 使用。

## 发布方式

这个仓库通过 GitHub Pages 发布：

1. 本地创建或编辑 Markdown 文件。
2. 使用相对链接组织本地文章和图片。
3. 提交变更并通过 PR 合并到 `main`。
4. GitHub Pages 自动构建并发布站点。
5. 构建完成后，线上站点更新到 <https://jackhai9.github.io/blog/>。

如果线上没有立刻变化，优先检查仓库 `Actions` 页面里的 `pages build and deployment` 工作流是否完成。

## GitHub Pages 设置

GitHub Pages 通常需要在仓库页面手动开启：

1. 打开仓库的 `Settings`。
2. 进入 `Pages`。
3. 选择发布分支和目录。
4. 保存设置。

这个仓库的发布目标是 `main` 分支，合并后由 GitHub Pages 自动完成构建和部署。

## 首页文件优先级

GitHub Pages 会优先使用仓库根目录的 `index.html` 或 `index.md` 作为首页。

如果没有这些文件，GitHub Pages 才会尝试使用 `README.md` 作为首页内容。

这个仓库显式使用 `index.md` 作为博客首页，所以 README 只作为仓库说明文档。

## Markdown 与 Jekyll

浏览器不会直接把 Markdown 当成网页渲染。GitHub Pages 会使用 Jekyll 这样的静态站点生成器，把 Markdown 转成 HTML，再交给浏览器显示。

本仓库没有引入完整自定义主题，只在必要位置覆盖默认行为：

- `_config.yml` 控制站点元数据。
- `_includes/head-custom.html` 处理 head 内的自定义资源和夜间模式。
- `_layouts/default.html` 覆盖默认页面骨架，去掉不需要的默认页脚。

## GitHub Actions 与部署

GitHub Pages 的构建和部署由 GitHub 自动执行。提交合并到发布分支后，可以在仓库的 `Actions` 页面看到 `pages build and deployment` 工作流。

这个工作流大致做几件事：

1. 拉取仓库内容。
2. 用 Jekyll 构建静态页面。
3. 上传构建产物。
4. 部署到 GitHub Pages。

如果构建失败，先看 Actions 日志；如果构建成功但线上页面没变，通常是浏览器缓存或 Pages 部署延迟。

## 本地写作辅助

本仓库提供一个可选的 Git hook，用来在提交 Markdown 文件前补写或更新文章日期：

- `本文创建日期`
- `最后更新日期`

安装方式：

```bash
bash scripts/setup-hooks.sh
```

这个 hook 适合文章文件。修改 README 或 docs 这类仓库说明文档时，如果不希望自动追加文章日期，可以在确认变更后使用 `git commit --no-verify`。

## SSH 配置

如果希望通过 SSH 和 GitHub 免密交互，可以参考 GitHub 官方文档：

- [检查本地现有的 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)
- [生成新的 SSH 密钥并添加到 ssh-agent](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [添加本地 SSH 密钥到 GitHub 账户](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## favicon

favicon 文件放在仓库根目录，当前文件是 `favicon.ico`。

Jekyll 页面里引用站点资源时，优先使用 `relative_url`，这样仓库名或 Pages 路径变化时不用手动改路径：

```html
<link rel="shortcut icon" type="image/x-icon" href="{{ '/favicon.ico' | relative_url }}">
```

## 站点标题与描述

Jekyll 默认可能使用仓库名作为站点名。如果要自定义站点标题和描述，可以在 `_config.yml` 中设置：

```yaml
title: 站点标题
description: 站点描述
lang: zh-CN
```
