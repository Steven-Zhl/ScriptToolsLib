#!/bin/bash

:<<COMMENT
这是一个简单的，用以清理缓存的Linux脚本
在使用前请先用"chmod +x <本文件>"来赋予脚本可执行权限
COMMENT

paramNum=$#; # 参数个数
paramList=$@; # 参数列表
version="1.0.0-beta"; # 版本号
autoRun=false; # 是否自动执行

help_zh_CN=$(cat <<- EOF
用法: clean_cache.sh [选项] <命令[<参数>]

选项:
    -h, --help          显示帮助信息
    -v, --version       显示版本信息
    -l, --list          列出所有可清理的应用

示例:
    clean_cache.sh      清理所有缓存
    clean_cache.sh      显示帮助信息
EOF
)
help_en_US=$(cat <<- EOF
Usage: clean_cache.sh [options] <command[<args>]

Options:
    -h, --help          Display this help message
    -v, --version       Display version information
    -l, --list          List all apps that can be cleaned

Examples:
    clean_cache.sh      Clean all caches
    clean_cache.sh      Display this help message
EOF
)
help=(['zh_CN.UTF-8']=$help_zh_CN ['en_US.UTF-8']=$help_en_US)

declare -A locale=(["zh_CN.UTF-8"]="zh_CN.UTF-8" ["en_US.UTF-8"]="en_US.UTF-8")
declare -A cachePaths=(
    ["paru"]="~/.cache/paru/clone"
    ["pip"]="~/.cache/pip"
    ["JetBrains"]="~/.cache/JetBrains"
    ["yarn"]="~/.cache/yarn"
    ) # 强制清除缓存，删除缓存路径下的文件
declare -A cacheCmds=(
    ["pip"]="pip cache purge" 
    ["jekyll"]="jekyll clean"
    ) # 调用程序自带的清理缓存命令

if test $paramNum -eq 0
then
    autoRun=true
else
    if test $paramList = "-h" || test $paramList = "--help"
    then
        echo ${help["$LANG"]}
    elif test $paramList = "-v" || test $paramList = "--version"
    then
        echo "v$version"
    elif test $paramList = "-l" || test $paramList = "--list"
    then
        for key in $(echo ${!cachePaths[*]})
        do
            echo $key
        done
    fi
fi
