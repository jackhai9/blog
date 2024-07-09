#!/bin/bash

### 为每个md文件自动添加创建日期和最后更新日期

FILE="$1"

echo "Processing file: $FILE"

if [ -z "$FILE" ]; then
  echo "Usage: $0 <markdown-file>"
  exit 1
fi

# 检查文件是否为 Markdown 文件
EXT="${FILE##*.}"
if [ "$EXT" != "md" ]; then
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
if ! grep -q "^> 本文创建日期:" "$FILE"; then
  echo -e "\n\n\n\n---\n\n> 本文创建日期: $CREATION_DATE\n>" >> "$FILE"
fi

# 删除已有的最后更新日期信息
sed -i '' -e '/^> 最后更新日期:/d' "$FILE"

# 删除文件末尾的空行
#sed -i '' -e :a -e '/^\n*$/{$d;N;};/\n$/ba' "$FILE"

# 追加新的最后更新日期信息到文件末尾
printf "> 最后更新日期: $LAST_UPDATE_DATE" >> "$FILE"


