# SubtitleTranslator

> 一个简单的字幕文件翻译工具
>
> 同时作为练习协程(`async`)的实验性项目
> 
> 协程真好用

## 格式适配

* [x] srt
* [ ] ass
* [ ] ssa
* [ ] lrc
* [ ] smi

## 接口适配

* [x] [谷歌翻译(网页)](https://translate.google.com)
* [ ] 谷歌翻译(API)
* [ ] 百度翻译(API)
* [ ] ChatGPT(API)

## 使用方法

> 其实[`main.py`](./main.py)就是一个简单的demo

1. 注意首先`from gevent import monkey` `monkey.patch_all()`
2. 实例化`Parser`和`Translator`，二者均支持在实例化和add方法中添加信息
3. `Parser.start()`，解析数据；`Parser.result()`，获取解析后的字幕数据(`list[Subtitle]`)
4. `Translator.add()`添加数据；`Translator.start()`执行翻译；`Translator.result()`，获取翻译后的字幕数据(`list[Subtitle]`)
5. 调用`dumpXXX()`(目前只有`dumpSrt()`)导出
