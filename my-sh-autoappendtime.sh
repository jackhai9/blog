#!/bin/bash

FILE=$1

if [ -z "$FILE" ]; then
  echo "Usage: $0 <markdown-file>"
  exit 1
fi

if [[ "$FILE" != *.txt ]]; then
  echo "This script only works with Markdown files (.md)."
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "File not found!"
  exit 1
fi

# 获取首次创建日期
CREATION_DATE=$(git log --diff-filter=A --follow --format=%ad --date=short -1 -- "$FILE")

# 获取最后更新日期
LAST_UPDATE_DATE=$(git log -1 --format=%ad --date=short -- "$FILE")

# 检查文件中是否已经有创建日期
if ! grep -q "^> 创建日期:" "$FILE"; then
  echo -e "\n> 创建日期: $CREATION_DATE" >> "$FILE"
fi

# 删除已有的最后更新日期信息
sed -i '' -e '/^> 最后更新日期:/d' "$FILE"

# 追加新的最后更新日期信息到文件末尾
printf "\n> 最后更新日期: $LAST_UPDATE_DATE" >> "$FILE"


