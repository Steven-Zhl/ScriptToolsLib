# Shell工具

## 目录

* [Shell工具](#shell工具)
  * [目录](#目录)
  * [常用指令.md](#常用指令md)
  * [BatteryReport.bat](#batteryreportbat)
  * [CleanCache.sh](#cleancachesh)
  * [Img2Webp.ps1](#img2webpps1)

## [常用指令.md](./常用指令.md)

> 记录一些常用的Powershell和cmd指令

* 详见[常用指令.md](./常用指令.md)

## [BatteryReport.bat](./BatteryReport.bat)

> 使用cmd指令生成电池状态报告文件，并自动打开

* **环境要求**
  * Windows
  * cmd

* **用法**
  * 双击直接运行

## [CleanCache.sh](./CleanCache.sh)

> 清理Linux系统中部分缓存
>
> 这个脚本是初学Shell时的练手作，也许会有些问题

* **环境要求**
  * Linux (以Arch为例)
  * bash/zsh

* **用法**
  * 在Bash或Zsh环境下，直接执行`CleanCache.sh`即可

## [Img2Webp.ps1](./Img2Webp.ps1)

> 调用FFmpeg，并行地将(jpg/jpeg/png/gif)转换为webp格式，并显示文件大小变化以及压缩率。

* **环境要求**
  * Windows 10及以上(因为更早的版本并不自带PowerShell)
  * PowerShell
  * FFmpeg (建议通过winget安装：`winget install Gyan.FFmpeg`)

* **注意事项**
  * 该脚本包括2个函数，`Img2Webp`和`Img2Webp_subfolder`。前者从当前目录下递归查找全部图片并转换，后者从当前目录的全部子目录下递归查找全部图片并转换。也就是说，后者不会转换当前目录下的图片，只会转换子目录下的图片，请按需使用。
    * 例：当你的文件结构为`<author>/<gallery>/<image>`时，可以跳转到`<author>`目录，使用`Img2Webp_subfolder`只转换全部`<gallery>`下的全部图片，使用`Img2Webp`则会转换全部`<author>`下的全部图片。
  * FFmpeg预设为`ffmpeg -i $inputFile -c:v libwebp -q:v 100 "$($inputFile.BaseName).webp" -loglevel quiet -n`，即：
    1. 有损压缩：`loseless`参数默认为0，即有损压缩
    2. 压缩质量：`-q:v 100`，即最高质量
    3. 输出路径：与原图片相同，文件名后缀改为`.webp`
    4. 文件冲突：`-n`，若输出文件已存在则不覆盖，直接跳过
    5. 日志等级：`-loglevel quiet`，不输出日志，静默模式
    * 这是我测试之后，比较符合我的需求的参数，有需要请自行调整。
  * 转换任务并未设定最大并发数，可能会导致CPU占用过高，建议在空闲时使用。
  * 转换完成后会自动删除原本的图片，若不需要删除，请自行注释掉`Remove-Item -LiteralPath $inputFile.FullName -Force # 删除原始图片`这一行。

* **用法**
  > 建议将此脚本的函数添加到PowerShell的配置文件中，以便直接调用(复制该脚本，在PowerShell中输入`notepad $PROFILE`，直接粘贴到打开的文件的最后即可)
  * `Img2Webp`：使用`cd`或`Set-Location`切换到图片所在目录，然后直接输入`Img2Webp`即可
  * `Img2Webp_subfolder`：使用`cd`或`Set-Location`切换到图片所在目录，然后直接输入`Img2Webp_subfolder`即可
