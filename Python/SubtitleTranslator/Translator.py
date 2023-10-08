import re
from copy import deepcopy
from html import unescape
from urllib import parse

import gevent
import requests
from gevent.queue import Queue
from tqdm import tqdm

from Declare import Config, Subtitle
from Declare import TransEngine


class Translator:
    def __init__(self, host: TransEngine, src=None, dst=None, content: list[Subtitle] = None) -> None:
        """
        :param host: 翻译服务
        :param src: 源语言
        :param dst: 目标语言
        :param content: 翻译内容，list[str]，每个元素为一段话
        """
        self._waitingQueue: list[Subtitle] = content if content else []
        self._finishQueue: list[Subtitle] = []
        # 翻译配置
        self._src = src if src else Config["language"]["src"]
        self._dst = dst if dst else Config["language"]["dst"]
        self._host = host  # 翻译引擎
        # 其他配置
        self.asyncNum = Config["asyncNums"]  # 各翻译引擎的并发数，为避免被ban，解析Web形式的线程数不宜过多
        self.headers = Config["headers"]
        self.proxies = Config["proxies"]

    def clear(self):
        """清空翻译队列和翻译结果"""
        self._waitingQueue = []
        self._finishQueue = []

    def clearWaitingQueue(self):
        """清空翻译队列"""
        self._waitingQueue = []

    def clearFinishQueue(self):
        """清空翻译结果"""
        self._finishQueue = []

    def result(self):
        """获取翻译结果"""
        return self._finishQueue

    def add(self, item: Subtitle or list[Subtitle]):
        if isinstance(item, Subtitle):
            self._waitingQueue.append(item)
        elif isinstance(item, list):
            self._waitingQueue.extend(item)

    def start(self):
        for item in self._waitingQueue:
            with tqdm(total=len(item.subtitles), desc="翻译进度") as pbar:
                if self._host == TransEngine.Google_Web:
                    self._google_web(item, pbar)
                else:
                    raise NotImplementedError("暂不支持该翻译引擎")

    def _google_web(self, item: Subtitle, pbar: tqdm):
        """
        调用谷歌翻译网页
        :param pbar: 进度条回调
        :return:
        """
        # 检查网络
        try:
            requests.get("https://translate.google.com/", headers=self.headers, proxies=self.proxies)
        except requests.exceptions.ConnectionError:
            print("网络连接失败，请检查网络连接")
            return
        contentQueue = Queue(items=tuple(item.subtitles))
        transDict = {}  # 原文-译文字典，用作结果回调
        asyncNum = self.asyncNum[TransEngine.Google_Web.name]
        gevent.joinall([gevent.spawn(self._google_web_async, contentQueue, transDict, pbar) for _ in range(asyncNum)])
        transItem = deepcopy(item)
        for i, sub in enumerate(transItem.subtitles):
            sub["content"] = transDict[sub["index"]]
            transItem.subtitles[i] = sub
        self._finishQueue.append(transItem)

    def _google_web_async(self, contentQueue: Queue, transDict: dict, pbarCallback: tqdm):
        """
        调用谷歌翻译网页时的功能函数
        :param contentQueue: 翻译内容队列
        :param transDict: 结果回调
        :param pbarCallback: 进度条回调
        :return:
        """
        while not contentQueue.empty():
            sub = contentQueue.get()
            index = sub["index"]
            src = "\n".join(sub["content"])
            url = f"https://translate.google.com/m?sl={self._src}&tl={self._dst}&q={parse.quote(src)}"
            try:
                data = requests.get(url, headers=self.headers, proxies=self.proxies).text
            except ConnectionResetError:
                contentQueue.put(sub)
                continue
            dst = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', data)
            if len(dst) > 0:
                transDict[index] = unescape(dst[0]).split("\n")
            else:
                transDict[index] = [""]
                print(f"翻译失败，原文：{sub}")
            pbarCallback.update(1)
            gevent.sleep(0.5)
