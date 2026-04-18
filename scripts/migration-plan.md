# 旧博客迁移方案

## 目标

- 将 `jackhai9.github.io/source/_posts` 中的历史文章迁移到当前 `blog` 仓库。
- 旧站 `jackhai9.github.io` 保持原样，继续在线，不删除、不覆盖、不重定向。
- 在新站中保留旧文的原始信息，尤其是原文时间、分类、标签、原文地址。
- 迁移过程必须可审、可复跑、可回滚，不能依赖手工逐篇复制。

## 现状结论

### 旧站

- 旧站是 Hexo 项目，文章位于 `jackhai9.github.io/source/_posts`。
- 旧文 front matter 中稳定存在 `title`、`date`，多数文章还有 `categories`、`tags`。
- 旧文原始时间只能从 front matter 的 `date` 取，Git 历史不反映文章原始发布/更新时间。

### 新站

- 新站是纯 Markdown + GitHub Pages 的轻量结构，文章主要放在 `blog/src`。
- 首页 `blog/index.md` 是手工维护的链接列表。
- `blog/scripts/autoappend-time.sh` 会在提交前自动追加或改写：
  - `> 本文创建日期:`
  - `> 最后更新日期:`
- 这意味着如果不做额外设计，迁移文章的“最后更新日期”会在提交时被改成迁移当天。

## 迁移原则

1. 原文时间直接使用旧文 front matter 中的 `date`。
2. 原始分类和标签直接使用旧文 front matter 中的 `categories`、`tags`。
3. 原文地址按旧站 Hexo permalink 规则恢复：
   `https://jackhai9.github.io/:year/:month/:day/:filename/`
4. 迁移脚本只写旧文的原始信息，不预填当前仓库的 `本文创建日期 / 最后更新日期`。
5. 当前仓库自己的 `本文创建日期 / 最后更新日期` 交给现有 pre-commit 在首次提交时补齐，用来表示新仓库里的文件生命周期。
6. 原始信息作为独立元数据写进迁移后的文章正文底部，避免被当前仓库的 pre-commit 钩子覆盖。
7. 旧站继续保留，迁移是复制，不是替换。

## 目录规划

- 旧文导入目录：`blog/src/legacy/`
- 迁移脚本：`blog/scripts/migrate_hexo_posts.py`
- 仓库布局前提：旧仓库 `jackhai9.github.io` 与本仓库 `blog/` 位于同一父目录下，脚本按默认相对路径 `../jackhai9.github.io/source/_posts` 定位旧文；若布局不同，用 `--source` 显式指定。

## 脚本参数

- `--dry-run`：只预览不写文件（默认行为）
- `--apply`：实际写入（缺这个参数就是预览）
- `--include <stem>`：只迁移指定源文件名（可重复，用于样例导出）
- `--source <dir>`：来源目录（默认 `../jackhai9.github.io/source/_posts`）
- `--output <dir>`：输出目录（默认 `src/legacy`）
- `--overwrite`：目标文件已存在时覆盖，不加则遇到冲突即报错退出
- `--write-index`：同时生成 `legacy/index.md` 归档入口，按发布日期倒序列出所有迁移文章，顶部含指向本方案的链接

## 内容转换规则

### 输入

- 来源目录：`jackhai9.github.io/source/_posts`
- 输入格式：Hexo Markdown + YAML front matter

### 输出

- 目标目录：`blog/src/legacy`
- 输出格式：普通 Markdown 文件，不保留 Hexo front matter

### 字段映射

- `title` -> 文档一级标题 `# title`
- `date` -> `原文时间: YYYY-MM-DD HH:mm:ss`
- `categories` -> `原文分类: ...`
- `tags` -> `原文标签: ...`
- 源文件名 -> 旧站 permalink 中的 slug
- 统一输出：上述四个字段包裹在 `<small><em style="color: #888">...<br></em></small>` 里，和正文间用 `---` 分隔，视觉上弱于当前仓库的本文创建/更新日期块
- 当前仓库时间 -> 由 pre-commit 在首次提交时写入 `> 本文创建日期:` 和 `> 最后更新日期:`

### 正文清洗

- 删除 Hexo 的 `<!--more-->`
- 保留正文原始 Markdown 内容
- 修复明显缺少协议头的裸链接，例如：
  - `msdn.itellyou.cn/` -> `https://msdn.itellyou.cn/`
  - `localhost:4000` -> `http://localhost:4000`
- 针对 `layout: photo` 文章，把 `photos:` 列表转成普通 Markdown 图片列表
- 文章含 `qiniudn.com` / `clouddn.com`（旧七牛测试域名，已失效）时，自动在文章顶部插入一行提示，说明图片因域名失效而无法显示，避免读者误认为是渲染 bug

## 执行流程

### Phase 1: 预览

只跑预览，不写文件：

```bash
cd blog
python3 scripts/migrate_hexo_posts.py --dry-run
```

检查点：

- 识别到的文章总数是否正确
- 输出路径是否都在 `src/legacy/`
- 原文时间和原文地址是否正确生成

### Phase 2: 样例导出

先导出 1 篇或少量文章到临时目录审核：

```bash
cd blog
python3 scripts/migrate_hexo_posts.py \
  --apply \
  --include 转投hexo-使用hexo在github写博客 \
  --output /tmp/blog-migration-sample
```

检查点：

- 一级标题是否正确
- `<!--more-->` 是否被删除
- 原始信息区块是否完整
- 中文文件名和链接是否正常

### Phase 3: 全量导入

确认样例通过后再写入仓库：

```bash
cd blog
python3 scripts/migrate_hexo_posts.py --apply --write-index
```

检查点：

- `src/legacy/` 下文章数量正确
- 自动生成的 `src/legacy/index.md` 可直接浏览
- 未覆盖现有 `src/*.md`

### Phase 4: 人工审阅

- 检查是否有少数文章需要手工修正文案、链接或图片
- 决定哪些旧文要挂到首页，哪些只放在 `legacy/index.md`

### Phase 5: 提交与发布

- 提交迁移脚本
- 提交迁移后的文章
- 提交首页入口更新
- 等 GitHub Pages 自动构建完成后抽查线上页面

## 验收标准

- 旧站可正常访问，内容不变
- 新站存在可重复执行的迁移脚本
- 新站存在迁移方案文档，别人看完就能复跑
- 每篇迁移文章至少保留以下原始信息：
  - 原文时间
  - 原文分类
  - 原文标签
  - 原文地址
- 迁移不会覆盖 `blog/src` 下现有文章

## 风险与处理

### 风险 1：当前 pre-commit 会改写最后更新日期

处理：

- 脚本不写当前仓库的 `本文创建日期 / 最后更新日期`，由 pre-commit 在首次提交时按仓库规则补齐
- 原文时间作为独立元数据写在文章底部 `<small>` 块，不会被 pre-commit 覆盖

### 风险 2：旧文存在少量 Hexo 专有内容

处理：

- 脚本自动删除 `<!--more-->`
- `layout: photo` 自动转普通 Markdown 图片
- 极个别仍不理想的文章，迁移后再手工修

### 风险 3：旧文裸链接无法直接点击

处理：

- 脚本只修复明确像域名或 localhost 的链接
- 不猜测相对路径，不引入新的错误

## 回滚方案

- 脚本只写 `src/legacy/`，不改旧站仓库
- 如需回滚，删除 `src/legacy/` 下本次导入文件并回退首页入口即可
- 因为是复制迁移，回滚不影响旧站




---

> 本文创建日期: 2026-04-18
>
> 最后更新日期: 2026-04-18
