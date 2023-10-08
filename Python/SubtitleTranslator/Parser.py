import os
import re
from datetime import datetime

import chardet
from tabulate import tabulate

from Declare import Subtitle, SubtitleFormat


class Parser:
    def __init__(self, path: str or list[str] = None) -> None:
        """
        :param path: 字幕文件路径/字幕文件夹路径/字幕文件路径列表
        """
        self._waitingQueue: list[Subtitle] = []
        self._finishQueue: list[Subtitle] = []
        self.formatCount = {f: 0 for f in SubtitleFormat}
        if path:
            self.add(path)

    def _parseMetadata(self, filePath: str):
        """
        (预处理)解析字幕文件的元数据，返回一个Subtitle对象
        :param filePath:
        :return:
        """
        if filePath.split('.')[-1].lower() not in [f.name for f in SubtitleFormat]:
            return
        subtitle = Subtitle()
        filePath = filePath.replace("\\", "/")
        subtitle.filePath = filePath
        subtitle.fileName = os.path.basename(filePath)
        try:
            subtitle.format = SubtitleFormat[subtitle.fileName.split(".")[-1].lower()]
        except KeyError:
            subtitle.format = SubtitleFormat.UNKNOWN
            subtitle.parseable = False
        subtitle.size = os.path.getsize(filePath)
        with open(filePath, "rb") as f:
            content = f.read()
            subtitle.rows = len(content.splitlines())
            subtitle.originEncoding = chardet.detect(content)["encoding"]
            if subtitle.originEncoding:
                subtitle.text = content.decode(subtitle.originEncoding)
            else:
                subtitle.parseable = False
        self._waitingQueue.append(subtitle)

    def add(self, path: str or list[str]):
        """向字幕队列中添加字幕文件，若参数path为文件夹，则将其视为根目录，递归添加该目录下的所有字幕文件"""
        if isinstance(path, str):
            if not os.path.exists(path):
                raise FileNotFoundError(f"文件{path}不存在")
            if os.path.isdir(path):
                for f in os.listdir(path):
                    if os.path.isfile(os.path.join(path, f)):
                        self._parseMetadata(os.path.join(path, f))
            else:
                self._parseMetadata(path)
        elif isinstance(path, list):
            for p in path:
                self.add(p)
        else:
            raise TypeError("item应为str或list[str]")

    def dispUnparsedQueue(self):
        """
        展示等待队列
        :return:
        """
        header = Subtitle.briefInfoHeader()
        infoSheet = [[item.briefInfo()[key] for key in header] for item in self._waitingQueue]
        print(tabulate(infoSheet, header, tablefmt="grid"))

    def dispParsedQueue(self):
        """
        展示已解析队列
        :return:
        """
        header = Subtitle.briefInfoHeader()
        infoSheet = [[item.briefInfo()[key] for key in header] for item in self._finishQueue]
        print(tabulate(infoSheet, header, tablefmt="grid"))

    def start(self):
        for i in range(len(self._waitingQueue)):
            item = self._waitingQueue.pop()
            if item.format == SubtitleFormat.srt:
                self._parse_srt(item)
            else:
                raise NotImplementedError(f"暂不支持{item.fileName}的字幕格式")

    def result(self) -> list[Subtitle]:
        """
        获取字幕解析结果
        """
        return self._finishQueue

    def _parse_srt(self, item: Subtitle):
        """
        解析srt字幕文件
        :param item:
        :return: dict["index":str, "time":str, "content":list[str]]
        """
        contents = item.text.split("\n")
        epoch = {"content": []}  # 一条字幕
        for row in contents:
            if re.fullmatch("^\d+$", row.strip()):
                if "startTime" in epoch:  # 说明此时的subtitle是上一条字幕
                    item.subtitles.append(epoch)
                    epoch = {"content": [], "index": int(row.strip())}
                else:
                    epoch["index"] = row.strip()
            elif re.fullmatch("^[\d:]+,\d{3} --> [\d:]+,\d{3}$", row.strip()):
                time = row.strip().split(" --> ")
                epoch["startTime"] = datetime.strptime(time[0], "%H:%M:%S,%f")
                epoch["endTime"] = datetime.strptime(time[1], "%H:%M:%S,%f")
                epoch["duration"] = epoch["endTime"] - epoch["startTime"]
            elif row.strip() == "":
                continue
            else:
                epoch["content"].append(row.strip())
        item.subtitles.append(epoch)
        self._finishQueue.append(item)
