#!/bin/bash
## 预定义部分
IFS=' '                                                                     #默认分隔符
paragraphLine='-----------------------------------------------------------' #分隔线
testNetwork() {                                                             # 测试网络是否可用
    tuna_link="mirrors.tuna.tsinghua.edu.cn"
    us_ubuntu_link="us.archive.ubuntu.com"
    ping -c 1 -W 1 $tuna_link >/dev/null 2>&1 || return 1
    ping -c 1 -W 1 $us_ubuntu_link >/dev/null 2>&1 || return 1
    return 0
}
testPrivilege() { # 测试是否有root权限
    return $([ $EUID -ne 0 ] && echo 1 || echo 0)
}
installCascadiaCode() { # 安装CascadiaCode字体
    wget https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip -P ~/下载/ >/dev/null
    cd ~/下载
    unzip ./CascadirCode-2111.01.zip
    rm ./CascadirCode-2111.01.zip && rm -rf ./otf/ && rm -rf ./woff2 # 删除无用的文件
    cd ./ttf
    mv ./static/*.ttf ./ # 将static字体也放到当前目录
    if [ ! -d "/usr/share/fonts/custom" ]; then
        sudo mkdir /usr/share/fonts/custom
    fi
    sudo mv ./*.ttf /usr/share/fonts/custom/
    mkfontscale && mkfontdir && fc-cache -fv # 更新字体缓存
    cd ..
    rm -rf ./ttf
}
installCaskaydiaCoveNerdFont() {
    wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/CascadiaCode.zip -P ~/下载/ >/dev/null
    cd ~/下载
    unzip ./CascadiaCode.zip
    rm ./CascadiaCode.zip && rm ./LICENSE && rm ./readme.md && rm ./fonts.dir && rm ./fonts.scale # 删除无用的文件
    if [ ! -d "/usr/share/fonts/custom" ]; then
        sudo mkdir /usr/share/fonts/custom
    fi
    sudo mv ./*.ttf /usr/share/fonts/custom/
    mkfontscale && mkfontdir && fc-cache -fv # 更新字体缓存
}
installVSCode() { # 安装VSCode(不喜欢snap安装，所以这里是用apt安装的)
    sudo apt install software-properties-common apt-transport-https wget
    wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
    sudo apt update >/dev/null
    sudo apt install code >/dev/null
}
installMSEdge() {
    sudo apt install software-properties-common apt-transport-https wget
    wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
    sudo apt update >/dev/null
    sudo apt install microsoft-edge-stable >/dev/null
}
installGithubDesktop() {
    wget -qO - https://packagecloud.io/shiftkey/desktop/gpgkey | sudo tee /etc/apt/trusted.gpg.d/shiftkey-desktop.asc >/dev/null
    sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/shiftkey/desktop/any/ any main" > /etc/apt/sources.list.d/packagecloud-shiftky-desktop.list'
    sudo apt update >/dev/null
    sudo apt install github-desktop >/dev/null
}
## 0. 检查权限和网络
echo '>-0. Checking----------------------------------------------'
test_res=0

testPrivilege
temp=$?
test_res=$(($test_res + $temp))
if [ $temp -eq 0 ]; then
    echo "  已获取root权限"
else
    echo "  Exit: 请使用root权限运行此脚本"
    echo $paragraphLine
    exit 1
fi

testNetwork
temp=$?
test_res=$(($test_res + $temp))
if [ $temp -eq 0 ]; then
    echo "  网络环境正常"
else
    echo "  Exit: 网络不可用，请检查网络连接"
    echo $paragraphLine
    exit 1
fi
if [ $test_res -eq 0 ]; then
    echo "  预检查通过，开始正式安装"
else
    echo "  Exit: 未通过检查步骤"
    echo $paragraphLine
    exit 1
fi

## 1. 配置apt
echo '>-1. Apt config--------------------------------------------'

echo '  1.1 更新软件源....'
sudo apt update >/dev/null # 更新软件源
echo "  1.2 配置软件源：请选择要添加的软件源(可多选):
    1 [国外]Ubuntu美国镜像
    2 [国内]清华Tuna镜像
    3 [国内]阿里云镜像
    4 [国内]中科大Ustc镜像
    5 [国内]网易163镜像"
read -p '    使用空格分隔，置空为全选' temp
read -ra apt_repo_selection <<<$temp
if [ ${#apt_repo_selection[@]} -eq 0 ]; then
    echo "  未选择任何软件源，将添加全部镜像源"
    sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
    echo '  旧软件源已备份至/etc/apt/sources.list.bak'
    sudo cat ./apt_source/Ubuntu/23.04/sources.list >/etc/apt/sources.list
    sudo cat ./apt_source/Ubuntu/23.04/tuna.list >>/etc/apt/sources.list
    sudo cat ./apt_source/Ubuntu/23.04/aliyun.list >>/etc/apt/sources.list
    sudo cat ./apt_source/Ubuntu/23.04/ustc.list >>/etc/apt/sources.list
    sudo cat ./apt_source/Ubuntu/23.04/163.list >>/etc/apt/sources.list
    echo "  添加完成"
else
    sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
    echo '  旧软件源已备份至/etc/apt/sources.list.bak'
    for i in "${apt_repo_selection[@]}"; do
        case $i in
        1)
            echo "    添加Ubuntu美国镜像"
            sudo cat ./apt_source/Ubuntu/23.04/sources.list >>/etc/apt/sources.list
            ;;
        2)
            echo "    添加清华Tuna镜像"
            sudo cat ./apt_source/Ubuntu/23.04/tuna.list >>/etc/apt/sources.list
            ;;
        3)
            echo "    添加阿里云镜像"
            sudo cat ./apt_source/Ubuntu/23.04/aliyun.list >>/etc/apt/sources.list
            ;;
        4)
            echo "    添加中科大Ustc镜像"
            sudo cat ./apt_source/Ubuntu/23.04/ustc.list >>/etc/apt/sources.list
            ;;
        5)
            echo "    添加网易163镜像"
            sudo cat ./apt_source/Ubuntu/23.04/163.list >>/etc/apt/sources.list
            ;;
        *)
            echo "    未知的选项，跳过"
            ;;
        esac
    done
    echo "  添加完成"
fi
echo '  1.3 更新软件源....'
sudo apt update >/dev/null # 更新软件源
echo '  1.4 更新可更新的软件，新系统该过程可能持续时间较长....'
sudo apt upgrade >/dev/null # 自动更新可更新的软件
echo '  1.5 清理无用的软件包....'
sudo apt autoremove # 自动清理无用的软件包

## 2. 安装一些基本软件
echo '>-2. Install some basic softwares--------------------------------------------'

echo '  2.1 安装Vim'
sudo apt install vim >/dev/null
echo '  2.2 安装Git'
sudo apt install git >/dev/null
echo '  2.3 安装Wget和Curl'
sudo apt install wget >/dev/null && sudo apt install curl >/dev/null

## 3. 下载并安装字体
echo '>-3. Download fonts----------------------------------------------------------'

echo '  3.1 安装Cascadia Code'
installCascadiaCode
echo '  3.2 安装Caskaydia Cove Nerd Font'
installCaskaydiaCoveNerdFont

## 4. 安装配置Zsh
echo '>-4. Zsh config--------------------------------------------------------------'

echo '  安装zsh'
sudo apt install zsh >/dev/null
git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
sudo chsh -s /usr/bin/zsh                                                                                                                        # 但似乎在默认shell中仍然会启用Bash，需要添加默认启动命令
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k >/dev/null          # 下载powerlevel10k主题
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions >/dev/null             # 下载zsh-autosuggestions插件
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting >/dev/null # 下载zsh-syntax-highlighting插件
sudo cp ./zshrc ~/.zshrc
source ~/.zshrc
zsh # 配置oh-my-zsh powerlevel10k

## 5. 安装部分微软软件
echo '>-5. Install some Microsoft softwares-----------------------------------------'

echo '  5.1 安装Visual Studio Code'
installVSCode
echo '  5.2 安装Microsoft Edge'
installMSEdge
echo '  5.3 安装Github Desktop'
installGithubDesktop
echo '  5.4 安装Microsoft To Do(Unofficial)'
snap install microsoft-todo-unofficial
## 创建一些目录
cd ~
mkdir Projects && cd ./Projects
mkdir Python && mkdir Jekyll && mkdir Database

## 安装其他软件
sudo apt install aria2 # Aria2，下载工具
sudo apt install unrar
sudo apt install vlc # Linux上最好的视频播放器
sudo apt install vsftpd # FTP服务器工具
systemctl start vsftpd.service
sudo apt install mysql-server
systemctl start mysql.service
sudo apt install ruby >/dev/null
sudo apt install ruby-dev >/dev/null
sudo apt install gem >/dev/null
sudo apt install jekyll >/dev/null
sudo gem install jekyll-paginate >/dev/null
wget https://dldir1.qq.com/qqfile/qq/QQNT/b69de82d/linuxqq_3.2.1-17153_amd64.deb -P ./下载/
# aria2配置参考这篇文章: https://jasonkayzk.github.io/2020/05/01/Aria2%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AE/
# 以及这个：https://owenyk.github.io/2021/06/22/systemctl%E7%AE%A1%E7%90%86%E6%96%B9%E5%BC%8F%E4%B8%8B%E8%AE%BE%E7%BD%AEaria2%E5%BC%80%E6%9C%BA%E5%90%AF%E5%8A%A8/
sudo apt install baobab # 磁盘分析工具
# aria2的tracker参考这个：

# Alist安装
curl -fsSL "https://alist.nn.ci/v3.sh" | bash -s install
snap install datagrip --classic             # 安装datagrip
snap install pycharm-professional --classic # 安装pycharm
##  一些静态资源
wget --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" --header="Accept-Encoding: gzip, deflate, br" --header="Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2" --header="Cache-Control: no-cache" --header="Connection: keep-alive" --header="Host: i.pximg.net" --header="Pragma: no-cache" --header="Referer: https://www.pixiv.net/" --header="Sec-Fetch-Dest: document" --header="Sec-Fetch-Mode: navigate" --header="Sec-Fetch-Site: cross-site" --header="Sec-Fetch-User: ?1" --header="TE: trailers" --header="Upgrade-Insecure-Requests: 1" --header="User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0" -P /home/steven/图片/ https://i.pximg.net/img-original/img/2019/12/12/22/03/54/78262885_p0.jpg # 我最喜欢的头像
wget --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" --header="Accept-Encoding: gzip, deflate, br" --header="Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2" --header="Cache-Control: no-cache" --header="Connection: keep-alive" --header="Host: i.pximg.net" --header="Pragma: no-cache" --header="Referer: https://www.pixiv.net/" --header="Sec-Fetch-Dest: document" --header="Sec-Fetch-Mode: navigate" --header="Sec-Fetch-Site: cross-site" --header="Sec-Fetch-User: ?1" --header="TE: trailers" --header="Upgrade-Insecure-Requests: 1" --header="User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0" -P /home/steven/图片/ https://i.pximg.net/img-original/img/2020/09/13/18/40/12/84349056_p3.jpg # 某个很棒的深色壁纸
## References
function showReferences() {
    declare -A refList
    refList["Bash"]="Bash拆分字符串 <https://www.yiibai.com/bash/bash-split-string.html>"
    refList["Zsh"]="Oh My Zsh, 『 安装 & 配置 』 <https://zhuanlan.zhihu.com/p/35283688>"
    refList["Apt_SourceList"]="Ubuntu 23.04、22.04、20.04、18.04国内源--阿里云、中科大、163、清华更新源 <https://blog.csdn.net/yinminsumeng/article/details/128625827>"
    refList["Apt_AddSource"]="在 Ubuntu 上如何添加 Apt 软件源 <https://cloud.tencent.com/developer/article/1626188>"
    refList["Apt_AddVSCode"]="Ubuntu从apt源中安装vscode <https://www.cnblogs.com/asialu/p/16002863.html>"
    refList["Apt_AddEdge"]="如何在Ubuntu 20.04安装Microsoft Edge浏览器 <https://www.myfreax.com/how-to-install-edge-browser-on-ubuntu-20-04/>"
    refList["Apt_AddGithub"]="ubuntu安装github desktop <https://zhuanlan.zhihu.com/p/397115131>"
    echo ${refList["Bash"]}
    echo $paragraphLine
}

showReferences
