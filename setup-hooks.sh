# setup-hooks.sh

# 复制 hooks 目录中的所有文件到 .git/hooks 目录中
cp hooks/* .git/hooks/

# 为所有 Git hooks 文件添加执行权限
chmod +x .git/hooks/*

