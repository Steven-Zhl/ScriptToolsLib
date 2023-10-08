import os
from enum import Enum

import yaml


def config() -> dict:
    if os.path.exists(os.path.join(os.getcwd(), "myconfig.yaml")):
        with open(os.path.join(os.getcwd(), "myconfig.yaml"), "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif os.path.exists(os.path.join(os.getcwd(), "config.yaml")):
        with open(os.path.join(os.getcwd(), "config.yaml"), "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise FileNotFoundError("未找到配置文件，请确保根目录下存在'myconfig.yaml'或'config.yaml'")


Config = config()


class UnknownCharsetError(Exception):
    """未知的字符集"""

    def __init__(self, filePath: str):
        self.filePath = filePath

    def __str__(self):
        return f"未知的字符集：{self.filePath}，无法获取其内容"


class SubtitleFormat(Enum):
    UNKNOWN = 0  # 未知格式
    srt = 1  # SubRip Subtitle，最常见的字幕格式之一
    ass = 2  # Advanced SubStation Alpha，最常见的字幕格式之一
    ssa = 3  # SubStation Alpha，也相对常见
    lrc = 4  # 常见于歌词的外置字幕
    smi = 5  # 较为少见，使用类xml的格式进行存储


class TransEngine(Enum):
    Google_Web = 1  # 解析https://translate.google.com的结果
    Google_API = 2  # 谷歌翻译的API
    Baidu_API = 3  # 百度翻译的API
    ChatGPT = 4  # 使用ChatGPT进行翻译


class Subtitle:  # 一个字幕文件，让它作为代码中描述整个字幕文件信息的数据结构。它应当是“所有支持的字幕的属性之并集”
    def __init__(self):
        self.fileName = ''  # 文件名
        self.filePath = ''  # 文件路径
        self.outputPath = ''  # 输出路径
        self.format = SubtitleFormat.UNKNOWN  # 字幕格式
        self.size: int = 0  # 文件大小(单位：字节)
        self.text = ''  # 字幕内容(未解析)
        self.subtitles: list[dict] = []  # 解析后的字幕内容
        self.parseable = True  # 是否可执行翻译
        self.rows = 0  # 文件行数
        self.originEncoding = ''  # 文件原始编码
        self.outputEncoding = ''  # 输出编码

    @staticmethod
    def briefInfoHeader() -> list[str]:
        """
        返回字幕文件的基本信息项
        :return: None
        """
        return ["文件名", "格式", "大小(Byte)", "行数", "编码", "能否解析"]

    def briefInfo(self) -> dict:
        """
        返回字幕文件的基本信息
        :return: None
        """
        return {
            "文件名": self.fileName,
            "格式": self.format.name,
            "大小(Byte)": self.size,
            "行数": self.rows,
            "编码": self.originEncoding,
            "能否解析": self.parseable
        }


def dumpSrt(content: Subtitle, filePath: str = None, encoding: str = None):
    if not filePath:
        if content.outputPath:
            filePath = content.outputPath
        else:
            filePath = content.filePath.replace(content.format.name, f"trans.{content.format.name}")
    with open(filePath, "w", encoding=encoding) as f:
        for i in content.subtitles:
            f.write(f"{i['index']}\n")
            f.write(f"{i['startTime'].strftime('%H:%M:%S,%f')[:-3]} --> {i['endTime'].strftime('%H:%M:%S,%f')[:-3]}\n")
            for c in i['content']:
                f.write(f"{c}\n")
            f.write("\n\n")
    return filePath
