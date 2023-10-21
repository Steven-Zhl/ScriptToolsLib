#!/bin/bash
function checkPrivilege() {
    echo "0. 检查权限...."
    if [ $EUID -eq 0 ]; then
        echo "  Error  : 请不要使用root权限运行此脚本"
        exit -1
    fi
}
function checkRequiredApps() {
    echo "1. 检查wget和xdg-user-dirs是否安装"
    updated=0 # 是否已经更新过apt源
    # 检查wget
    if command -v wget &>/dev/null; then
        echo "  wget已安装"
    else
        echo "  Warning: wget未安装，正在尝试安装wget"
        if (($updated == 0)); then
            sudo apt update >/dev/null
            updated=1
        fi
        sudo apt install wget -y >/dev/null
        if command -v wget &>/dev/null; then
            echo "  wget安装成功"
        else
            echo "  wget安装失败，请检查网络连接"
            exit -1
        fi
    fi
    # 检查xdg-user-dirs
    if xdg-user-dir DOWNLOAD &>/dev/null; then
        echo "  xdg-user-dirs已安装"
    else
        echo "  Warning: xdg-user-dirs未安装，正在尝试安装xdg-user-dirs"
        if (($updated == 0)); then
            sudo apt update >/dev/null
            updated=1
        fi
        sudo apt install xdg-user-dirs -y >/dev/null
        if xdg-user-dir DOWNLOAD &>/dev/null; then
            echo "  xdg-user-dirs安装成功"
        else
            echo "  xdg-user-dirs安装失败，请检查网络连接"
            exit -1
        fi
    fi
}
function queryInstallMethod() {
    echo "2. 请选择安装方式：
  1. 本地安装
  2. 在线安装"
    read -p "  请选择:[1/2]：" method
    return $method
}

echo "-----Clash for Windows(Linux)安装脚本-----"

checkPrivilege
checkRequiredApps
if [ ! -d $HOME"/cfw_temp" ]; then
    sudo mkdir $HOME"/cfw_temp"
fi
temp_dir=$HOME"/cfw_temp"
if [ ! -d "/opt/clash-for-windows-bin" ]; then
    sudo mkdir "/opt/clash-for-windows-bin"
fi
target_dir="/opt/clash-for-windows-bin"

queryInstallMethod # 选择安装方式
method=$?

if (($method == 1)); then
    echo "3. 请输入安装包路径或拖拽安装包："
    read -p "  路径：" pkg_path
    pkg_path=$(echo "$pkg_path" | sed -e "s/['\"]//g")
    if [ ! -f $pkg_path ]; then
        echo "  Error  : 文件不存在"
        exit -1
    fi
    echo "4. 安装中，请稍后..."
    folder_name=$(tar -tzf "$pkg_path" | head -n 1 | awk -F "/" '{print $1}')
    echo "  4.1  正在解压压缩包...."
    sudo tar -zxvf "$pkg_path" -C "$temp_dir" >/dev/null
    if [ ! -d "$temp_dir/$folder_name" ]; then
        echo "    Error  : 解压失败"
        exit -1
    else
        echo "    解压完成"
    fi
    sudo mv "$temp_dir/$folder_name/"* "$target_dir"
    echo "  4.2 尝试下载图标..."
    sudo wget "https://cdn.jsdelivr.net/gh/Dreamacro/clash@master/docs/logo.png" -T 8 -O "$target_dir/logo.png" -q
    if [ ! -f "$target_dir/logo.png" ]; then
        echo "    Error  : 下载图标失败"
    else
        echo "    下载图标成功"
    fi
    echo "  4.3 正在创建快捷方式..."
    echo "[Desktop Entry]
Name=Clash for Windows
Exec=$target_dir/cfw
Icon=$target_dir/logo.png
Terminal=false
Type=Application
Comment=A Windows/macOS/Linux GUI based on Clash and Electron.
Categories=Network;" | sudo tee /usr/share/applications/clash_for_windows.desktop >/dev/null
    if [ ! -f "/usr/share/applications/clash_for_windows.desktop" ]; then
        echo "    Error  : 创建快捷方式失败，请手动创建快捷方式："
        echo "             1. 在/usr/share/applications/路径下创建clash_for_windows.desktop文件"
        echo "             2. 将以下内容复制到clash_for_windows.desktop文件中"
        echo "[Desktop Entry]
Name=Clash for Windows
Exec=$target_dir/cfw
Icon=$target_dir/logo.png
Terminal=false
Type=Application
Comment=A Windows/macOS/Linux GUI based on Clash and Electron.
Categories=Network;"
        echo "             3. 保存，稍等或重启后即可在应用菜单中找到Clash for Windows"
    else
        echo "    创建快捷方式成功"
    fi
    echo "5. 清理临时文件..."
    sudo rm -rf "$temp_dir"
    echo "  清理完成"
    echo "安装完成"
elif (($method == 2)); then
    read -p "  请输入版本号(例：0.20.39)：" version
    echo "3. 正在尝试下载..."
    sudo wget "https://github.com/Fndroid/clash_for_windows_pkg/releases/download/$version/Clash.for.Windows-${version}-x64-linux.tar.gz" -O "$temp_dir/Clash.for.Windows-${version}-x64-linux.tar.gz"
    if [ ! -f "$temp_dir/Clash.for.Windows-${version}-x64-linux.tar.gz" ]; then
        echo "  Error  : 下载失败，请检查网络连接"
        exit -1
    else
        echo "  下载成功，正在安装..."
    fi
    if [ ! -f $pkg_path ]; then
        echo "  Error  : 文件不存在"
        exit -1
    fi
    pkg_path="$temp_dir/Clash.for.Windows-${version}-x64-linux.tar.gz"
    echo "4. 安装中，请稍后..."
    folder_name=$(tar -tzf "$pkg_path" | head -n 1 | awk -F "/" '{print $1}')
    echo "  4.1  正在解压压缩包...."
    sudo tar -zxvf "$pkg_path" -C "$temp_dir" >/dev/null
    if [ ! -d "$temp_dir/$folder_name" ]; then
        echo "    Error  : 解压失败"
        exit -1
    else
        echo "    解压完成"
    fi
    sudo mv "$temp_dir/$folder_name/"* "$target_dir"
    echo "  4.2 尝试下载图标..."
    sudo wget "https://cdn.jsdelivr.net/gh/Dreamacro/clash@master/docs/logo.png" -T 8 -O "$target_dir/logo.png" -q
    if [ ! -f "$target_dir/logo.png" ]; then
        echo "    Error  : 下载图标失败"
    else
        echo "    下载图标成功"
    fi
    echo "  4.3 正在创建快捷方式..."
    echo "[Desktop Entry]
Name=Clash for Windows
Exec=$target_dir/cfw
Icon=$target_dir/logo.png
Terminal=false
Type=Application
Comment=A Windows/macOS/Linux GUI based on Clash and Electron.
Categories=Network;" | sudo tee /usr/share/applications/clash_for_windows.desktop >/dev/null
    if [ ! -f "/usr/share/applications/clash_for_windows.desktop" ]; then
        echo "    Error  : 创建快捷方式失败，请手动创建快捷方式："
        echo "             1. 在/usr/share/applications/路径下创建clash_for_windows.desktop文件"
        echo "             2. 将以下内容复制到clash_for_windows.desktop文件中"
        echo "[Desktop Entry]
Name=Clash for Windows
Exec=$target_dir/cfw
Icon=$target_dir/logo.png
Terminal=false
Type=Application
Comment=A Windows/macOS/Linux GUI based on Clash and Electron.
Categories=Network;"
        echo "             3. 保存，稍等或重启后即可在应用菜单中找到Clash for Windows"
    else
        echo "    创建快捷方式成功"
    fi
    echo "5. 清理临时文件..."
    sudo rm -rf "$temp_dir"
    echo "  清理完成"
    echo "安装完成"
else
    echo "输入错误"
    exit -1
fi
