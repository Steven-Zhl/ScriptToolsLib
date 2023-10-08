# Python脚本

## 目录

* [Python脚本](#python脚本)
  * [目录](#目录)
  * [AutoRename.py](#autorenamepy)
  * [Bilibili\_Batch](#bilibili_batch)
  * [FxxkChromiumSecurity.py](#fxxkchromiumsecuritypy)
  * [M3U8\_Decrypt.py](#m3u8_decryptpy)
  * [SubtitleTranslator](#subtitletranslator)
  * [YNU\_大学生创新创业MOOC搜题](#ynu_大学生创新创业mooc搜题)
  * [YNU\_TimetableConvert](#ynu_timetableconvert)

## [AutoRename.py](./AutoRename.py)

> 一个用于批量重命名文件的脚本，目前只做了替换字符串，之后也许会支持正则表达式吧
>
> 说真的，这个脚本是初学Python时写的，功能比较烂。

### 功能

* 批量重命名文件

### 环境要求

* Python 3

### 用法

* 在Python环境中运行即可
* 目前提供了`bench`和`simple`两种运行模式，修改变量`mode`的值即可

### ChangeLog

* 2023-01-09
  * 完成一点点功能

## [Bilibili_Batch](./Bilibili_Batch/下载B站动漫弹幕.py)

> 针对哔哩哔哩弹幕的处理脚本

### 环境要求

* Python 3
  * requests
  * BeautifulSoup4
* [danmaku2ass.py](https://github.com/m13253/danmaku2ass/danmaku2ass.py)

### 用法

* 详见该脚本的[README.md](./Bilibili_Batch/README.md)

### ChangeLog

* 2022-11-03
  * 完成初步代码编写
* 2022-11-19
  * Update 下载B站动漫弹幕.py
* 2023-05-18
  * Update 下载B站视频弹幕.py

## [FxxkChromiumSecurity.py](./FxxkChromiumSecurity.py)

> * 一个用于显示Chromium浏览器中，账号密码数据库的工具（仅限于Windows端Chrome和Edge，但相信大多数人的主要浏览器都是这两者之一）
>
> * （Chromium在账号安全性的保护上有够偷懒，用数据库存账号密码没问题，虽然密码也加密了，但架不住密钥也直接放在本地）
>
> * 好在经过测试，这段代码要跑起来的要求还是挺高的：必须使用Python执行源码，并且需要以下全部库的支持。

    ⚠⚠注意：本文件仅用于学习交流，请勿用作非法用途，所造成的一切后果不承担相关责任。

### 环境要求

* Python 3
  * win32crypt
  * cryptography
  * base64
  * sqlite3
  * json

### 用法

* 在Python环境中运行即可

### ChangeLog

* 2023-01-09
  * 完成代码编写
* 2023-10-07
  * 修复了一点点bug
  * 2023-10-07测试，Edge和Chrome仍然在摆烂

## [M3U8_Decrypt.py](./M3U8_Decrypt.py)

> 根据m3u8文件合并视频碎片，并使用Python.Crypto进行文件的AES解密、合并(有需要的话)

<details>
  <summary>About it....</summary>
  可以说这个脚本完全是为了解决UC下载视频的问题而写的。曾经在UC上下载视频，格式是<code>m3u8</code>，且使用了<code>AES-128</code>加密，使得大多数本支持<code>ts</code>格式的视频软件也无法正常播放。不过发现现在UC自带转mp4功能了，并且取消了加密，所以这个脚本就没什么用了....
</details>

### 环境要求

* Python 3
  * Crypto
    * > 注：使用pip安装(`pip install crypto`)后，需要找到解释器路径下的`Lib/site-packages/crypto`，将`crypto`修改为`Crypto`，才能够正常调用

### 用法

* 不写了，因为甚至找不到一个文件来用这个脚本

### ChangeLog

* 2022-08-28
  * 完成代码编写

## [SubtitleTranslator](./SubtitleTranslator/)

> 简单的字幕翻译工具，使用谷歌翻译网页版

### 环境要求

* Python 3
  * gevent
  * yaml
  * tqdm

### 用法

* 详见本项目的[README.md](./SubtitleTranslator/README.md)

### ChangeLog

* 2023-07-19
  * 初步代码编写(谷歌翻译网页版)

## [YNU_大学生创新创业MOOC搜题](./YNU_大学生创新创业MOOC搜题/)

> 初次玩Python爬虫时做的一个练手程序，当时可以使用“精华吧”搜索“大学生创新创业”MOOC的课后题
>
> 但是目前，由于该网站增强了反爬手段，已经无法使用了，这个脚本就放在这当个纪念吧

### 环境要求

* Python 3
  * BeautifulSoup4
  * urllib3

### 用法

* 详见本项目的[README.md](./YNU_大学生创新创业MOOC搜题/README.md)

### ChangeLog

* 2022-01-09
  * 完成代码编写

## [YNU_TimetableConvert](./YNU_TimetableConvert/)

> 将YNU教务系统中的课程表进行格式转换的脚本，使之适应各种第三方日程类应用

### 环境要求

* Python 3
  * openpyxl
  * csv

### 用法

* 详见该脚本的[README.md](./YNU_TimetableConvert/README.md)

### ChangeLog

* 2022-12-26
  * 完成代码编写
* 2023-02-20
  * 修复了2个bug
