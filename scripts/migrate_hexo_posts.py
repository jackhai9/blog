#!/usr/bin/env python3

"""Migrate Hexo posts into the current Markdown-only blog structure."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_SOURCE = Path("../jackhai9.github.io/source/_posts")
DEFAULT_OUTPUT = Path("src/legacy")
OLD_SITE_BASE_URL = "https://jackhai9.github.io"
MORE_TAG_RE = re.compile(r"(?m)^[ \t\u3000]*<!--more-+>[ \t]*\n?")
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
# Image CDNs that are confirmed dead (七牛测试域名早已下线，Wayback 也无副本).
DEAD_IMAGE_HOST_RE = re.compile(r"(?:qiniudn\.com|clouddn\.com)", re.IGNORECASE)
DEAD_IMAGE_NOTICE = (
    "> 本文从旧博客迁移而来，当年使用的七牛测试域名已失效，部分图片无法显示。"
)


@dataclass
class LegacyPost:
    source_path: Path
    source_reference: str
    title: str
    published_at: datetime
    categories: list[str]
    tags: list[str]
    layout: str | None
    photos: list[str]
    body: str

    @property
    def source_stem(self) -> str:
        return self.source_path.stem

    @property
    def destination_name(self) -> str:
        return self.source_path.name

    @property
    def original_url(self) -> str:
        return (
            f"{OLD_SITE_BASE_URL}/"
            f"{self.published_at:%Y/%m/%d}/"
            f"{self.source_stem}/"
        )

    @property
    def created_date(self) -> str:
        return self.published_at.strftime("%Y-%m-%d")

    @property
    def published_timestamp(self) -> str:
        return self.published_at.strftime("%Y-%m-%d %H:%M:%S")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or migrate Hexo posts into the current blog repository."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Hexo source/_posts directory.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output directory for migrated Markdown files.",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Only migrate the post with the matching source stem. Repeatable.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite destination files if they already exist.",
    )
    parser.add_argument(
        "--write-index",
        action="store_true",
        help="Generate legacy index.md in the output directory when applying.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write files to disk. Without this flag the script only prints a preview.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Explicitly run in preview mode.",
    )
    return parser.parse_args()


def parse_front_matter(raw_text: str) -> tuple[dict[str, object], str]:
    lines = raw_text.splitlines()
    start_index = 0
    closing_index = None

    if lines and lines[0].strip() == "---":
        start_index = 1
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                closing_index = index
                break
    else:
        for index, line in enumerate(lines):
            if line.strip() == "---":
                closing_index = index
                break

    if closing_index is None:
        raise ValueError("Could not find the closing front matter marker.")

    metadata: dict[str, object] = {}
    current_key: str | None = None

    for line in lines[start_index:closing_index]:
        if not line.strip():
            continue

        if line.startswith("  - ") and current_key is not None:
            metadata.setdefault(current_key, [])
            values = metadata[current_key]
            if not isinstance(values, list):
                raise ValueError(f"Key {current_key} unexpectedly switched types.")
            values.append(line[4:].strip())
            continue

        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        current_key = key

        if value == "":
            metadata[key] = []
        else:
            metadata[key] = value

    body = "\n".join(lines[closing_index + 1 :]).lstrip("\n")
    return metadata, body


def parse_datetime(raw_date: str) -> datetime:
    match = re.match(
        r"^(\d{4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})$",
        raw_date,
    )
    if not match:
        raise ValueError(f"Unsupported date format: {raw_date}")

    year, month, day, hour, minute, second = (int(part) for part in match.groups())
    return datetime(year, month, day, hour, minute, second)


def normalize_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [item.strip() for item in value if item.strip()]

    if value is None:
        return []

    text = str(value).strip()
    if not text:
        return []

    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [part.strip() for part in inner.split(",") if part.strip()]

    return [text]


def normalize_link_target(target: str) -> str:
    if re.match(r"^(localhost|127\.0\.0\.1)(:\d+)?(/.*)?$", target):
        return f"http://{target}"
    # Only repair clear bare-site URLs. Relative file links like "note.md" must remain untouched.
    if re.match(
        r"^(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?::\d+)?(?:/.*|\?.*|#.*)$",
        target,
    ):
        return f"https://{target}"
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return target
    if target.startswith(("/", "#", "./", "../")):
        return target
    return target


def normalize_body(body: str) -> str:
    body = body.replace("\r\n", "\n")
    body = MORE_TAG_RE.sub("", body)

    def replace_link(match: re.Match[str]) -> str:
        prefix, target, suffix = match.groups()
        return f"{prefix}{normalize_link_target(target.strip())}{suffix}"

    body = MARKDOWN_LINK_RE.sub(replace_link, body)
    return body.strip()


def build_post(source_path: Path) -> LegacyPost:
    metadata, body = parse_front_matter(source_path.read_text(encoding="utf-8"))
    raw_date = str(metadata.get("date", "")).strip()
    if not raw_date:
        raise ValueError(f"Missing date in {source_path}")

    published_at = parse_datetime(raw_date)
    title = str(metadata.get("title", "")).strip() or source_path.stem
    layout = str(metadata.get("layout", "")).strip() or None
    photos = normalize_list(metadata.get("photos"))

    return LegacyPost(
        source_path=source_path,
        source_reference="",
        title=title,
        published_at=published_at,
        categories=normalize_list(metadata.get("categories")),
        tags=normalize_list(metadata.get("tags")),
        layout=layout,
        photos=photos,
        body=normalize_body(body),
    )


def format_metadata_line(label: str, values: list[str]) -> str:
    return f"> {label}: {', '.join(values) if values else '无'}"


def has_dead_images(post: LegacyPost) -> bool:
    if any(DEAD_IMAGE_HOST_RE.search(url) for url in post.photos):
        return True
    return bool(DEAD_IMAGE_HOST_RE.search(post.body))


def render_post(post: LegacyPost) -> str:
    lines: list[str] = [f"# {post.title}", ""]

    if has_dead_images(post):
        lines.append(DEAD_IMAGE_NOTICE)
        lines.append("")

    if post.layout == "photo" and post.photos:
        lines.append("> This post originally used Hexo photo layout.")
        lines.append("")
        for photo in post.photos:
            lines.append(f"![]({photo})")
            lines.append("")

    if post.body:
        lines.append(post.body)
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            f"> 原始发布时间: {post.published_timestamp}",
            format_metadata_line("原文分类", post.categories),
            format_metadata_line("原文标签", post.tags),
            f"> 原文地址: {post.original_url}",
            f"> 原始来源文件: {post.source_reference}",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def render_index(posts: list[LegacyPost], output_dir: Path) -> str:
    lines = [
        "# 旧博客归档",
        "",
        "以下文章由迁移脚本从 `jackhai9.github.io/source/_posts` 生成到当前仓库。",
        "",
        "迁移规则和脚本说明见：[旧博客迁移方案](../旧博客迁移方案.md)。",
        "",
    ]

    for post in sorted(posts, key=lambda item: item.published_at, reverse=True):
        lines.append(
            f"- [{post.title}]({post.destination_name}) ({post.published_at:%Y-%m-%d})"
        )

    return "\n".join(lines).rstrip() + "\n"


def collect_posts(source_dir: Path, includes: set[str]) -> list[LegacyPost]:
    posts = []
    for source_path in sorted(source_dir.glob("*.md")):
        if includes and source_path.stem not in includes:
            continue
        post = build_post(source_path)
        relative_path = source_path.relative_to(source_dir.parent.parent).as_posix()
        post.source_reference = (
            f"{source_dir.parent.parent.name}/{relative_path}"
        )
        posts.append(post)
    return posts


def ensure_output_path(output_path: Path, overwrite: bool) -> None:
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Destination already exists: {output_path}. Use --overwrite to replace it."
        )


def main() -> int:
    args = parse_args()
    source_dir = args.source.resolve()
    output_dir = args.output.resolve()
    includes = set(args.include)

    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source directory does not exist: {source_dir}")

    posts = collect_posts(source_dir, includes)
    if not posts:
        raise RuntimeError("No posts matched the current selection.")

    if args.apply and args.dry_run:
        raise RuntimeError("Use either --apply or --dry-run, not both.")

    apply_mode = args.apply

    print(
        f"{'Applying' if apply_mode else 'Previewing'} migration for "
        f"{len(posts)} post(s) from {source_dir} to {output_dir}"
    )

    if not apply_mode:
        for post in posts:
            print(
                f"- {post.source_path.name} -> {output_dir / post.destination_name} | "
                f"published {post.published_timestamp} | original {post.original_url}"
            )
        if args.write_index:
            print(f"- index.md -> {output_dir / 'index.md'}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)

    for post in posts:
        destination_path = output_dir / post.destination_name
        ensure_output_path(destination_path, args.overwrite)
        destination_path.write_text(render_post(post), encoding="utf-8")
        print(f"Wrote {destination_path}")

    if args.write_index:
        index_path = output_dir / "index.md"
        ensure_output_path(index_path, args.overwrite)
        index_path.write_text(render_index(posts, output_dir), encoding="utf-8")
        print(f"Wrote {index_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
