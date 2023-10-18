temp_dir=install_cfw_script
function queryInstallMethod(){
echo "2. 请选择安装方式：
    1. 本地安装
    2. 在线安装"
read -p "请选择:[1/2]：" method
return $method
}
function checkWget(){
    echo "1. 检查wget是否安装"
    if [$(which curl) == ""]
    then
        echo "  wget未安装，正在尝试安装wget"
        sudo apt update
        sudo apt install wget # 先更新apt，再安装wget
        if [$(which curl) == ""]
        then
            echo "  安装失败，请检查网络连接"
            exit -1
        else
            echo "  安装完成"
        fi
    else
        echo "  wget已安装"
    fi 
}

echo "-----Clash for Windows(Linux)安装脚本-----"

# 检查root权限
if [ $EUID -ne 0 ]
then
    echo "请使用root权限运行此脚本"
    exit -1
fi

# 选择安装方式
checkWget
queryInstallMethod
method=$?
echo $method

if (($method == 1))
then
    echo "请输入安装包路径："
    read -p "路径：" path
    if [ ! -f $path ]
    then
        echo "文件不存在"
        exit -1
    fi
    echo "正在安装，请稍后..."
    if [ ! -d /bin/clash-for-windows ]
    then
        mkdir /bin/clash-for-windows
    fi
    echo "安装完成"
elif (($method == 2))
then
    echo "正在安装，请稍后..."
    wget "https://" -O $(xdg-user-dir DOWNLOAD)/$temp_dir/
else
    echo "输入错误"
    exit -1
fi
