# MySQL脚本

## 目录

* [MySQL脚本](#mysql脚本)
  * [目录](#目录)
  * [URL\_UNQUOTE.sql](#url_unquotesql)
    * [功能](#功能)
    * [环境要求](#环境要求)
    * [用法](#用法)

## [URL_UNQUOTE.sql](./URL_UNQUOTE.sql)

> 在一些教程中会提到MySQL自带了一个`URL_UNQUOTE`函数，但实际上在我使用的MySQL中并没有，因此自己写了一个。

### 功能

* 将参数中符合URL编码的部分解码

### 环境要求

> 编写&测试环境，并非强制要求

* MySQL Community Server 8.0.36

### 用法

* 登录具有`CREATE FUNCTION`权限的用户，如`root`。
* 将`URL_UNQUOTE.sql`中的内容复制到MySQL的终端中直接执行即可。
