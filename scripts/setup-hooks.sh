# setup-hooks.sh

# Resolve repo root so this script works from any cwd.
cd "$(dirname "$0")/.." || exit 1

# 复制 hooks 目录中的所有文件到 .git/hooks 目录中
cp hooks/* .git/hooks/

# 为所有 Git hooks 文件添加执行权限
chmod +x .git/hooks/*

