from gevent import monkey

monkey.patch_all()

from Declare import TransEngine, dumpSrt
from Parser import Parser
from Translator import Translator

if __name__ == '__main__':
    parser = Parser("在此填写文件或文件夹名(目前仅支持srt文件)")
    translator = Translator(TransEngine.Google_Web, src="ja", dst="zh-CN")
    parser.start()

    translator.add(parser.result())
    translator.start()
    res = translator.result()
    dumpSrt(res[0], filePath="E:/Desktop/test.srt")  # 导出为srt文件
