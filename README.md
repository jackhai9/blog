# Markdown Blog

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> | English
</p>

This repository contains a Markdown-first personal blog published with GitHub Pages. The main workflow is intentionally simple: write Markdown files, commit them to `main`, and let GitHub Pages render the site.

Live site: [jackhai9.github.io/blog](https://jackhai9.github.io/blog/)

## What This Repository Is For

- Keep blog posts as plain Markdown files.
- Publish the repository directly through GitHub Pages.
- Avoid the heavier Hexo workflow used by the older `jackhai9.github.io` repository.
- Keep images, links, and article structure close to the source content.

## Repository Layout

- `index.md` is the blog entry page.
- `src/` stores article Markdown files.
- `_config.yml` configures the GitHub Pages/Jekyll site metadata.
- `_layouts/default.html` overrides the default Primer layout and removes the license-triggered footer.
- `_includes/head-custom.html` customizes the generated HTML head, including the favicon and dark mode toggle.
- `docs/additional-notes.md` keeps additional project notes in Chinese.
- `scripts/` contains local maintenance helpers for post metadata and migration.
- `hooks/` contains Git hook templates used by `scripts/setup-hooks.sh`.

## Writing Workflow

1. Create or edit Markdown files under `src/`.
2. Use relative links for local articles and images.
3. Commit the Markdown changes to `main`.
4. GitHub Pages builds and publishes the site.

Optional local hook setup:

```bash
bash scripts/setup-hooks.sh
```

The hook updates article creation and last-updated metadata before commits.
For README or docs-only commits, see [`docs/additional-notes.md`](docs/additional-notes.md#提交项目文档时的-hook-说明) before committing.

## Legacy Blog

The older Hexo-based blog lives in [`jackhai9/jackhai9.github.io`](https://github.com/jackhai9/jackhai9.github.io).

## License

Unless otherwise noted, prose content is licensed under Creative Commons Attribution 4.0 International. Local automation scripts are available under the MIT terms described in [LICENSE](LICENSE).
