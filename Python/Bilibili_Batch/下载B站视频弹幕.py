import os
import re
import subprocess
import requests
from bs4 import BeautifulSoup as BS

from xml2ass import Danmaku2ASS as tr


class Download:
    def __init__(self, url, savepath, width=1920, height=1080):
        self.title = ""  # 视频标题
        self.author = ""  # 视频作者
        self.cid = ""  # 视频cid
        self.videoUrl = url  # 视频地址
        self.barrageUrl = ""  # 弹幕地址
        self.savepath = savepath  # 保存路径
        self.filepath = ""  # 文件路径
        self.html = ""  # html内容
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.proxies = {
            'http': 'http://127.0.0.1:port',
            'https': 'http://127.0.0.1:port'
        }
        self.width = width  # 视频宽度
        self.height = height  # 视频高度
        # 如需调用BBDown下载视频，填写BBDown.exe的路径
        self.BBDownPath = "D:/FileTools/BBDown/BBDown.exe"

    def getHtml(self, proxies=False):
        # 获取html内容
        res = requests.get(self.videoUrl, headers=self.headers, proxies=self.proxies) if proxies else requests.get(
            self.videoUrl, headers=self.headers)

        self.html = res.text

    def getMessage(self):
        soup = BS(self.html, 'html.parser')
        self.title = str(soup.find(name="title").contents[0])
        self.title = self.title.replace('_哔哩哔哩_bilibili', '').strip()
        self.title = re.sub(r'[\/\\\:\*\?\"\<\>\|]', ' ',
                            self.title)  # 替换掉不可用于文件名的字符
        self.cid = re.findall(r'"cid":(.*?),', self.html)[0]
        if soup.find(class_="normal-members-container"):  # 多个UP主
            members = soup.find(
                class_="normal-members-container").find_all(class_="upname")
            self.author = " ; ".join(
                [partner.text for partner in members])  # 多个UP主的分割符
        else:  # 单个UP主
            self.author = soup.find_all(class_="up-name")[0].text
            self.author = self.author.replace("\n", "").strip()
        self.author = re.sub(r"[\/\\\:\*\?\"\<\>\|]",
                             " ", self.author)  # 替换掉不可用于文件名的字符
        # 这就是B站存放弹幕的文件啦
        barrageUrl = f'https://comment.bilibili.com/{self.cid}.xml'
        self.barrageUrl = barrageUrl

    def download(self, proxies=False):
        res = requests.get(self.barrageUrl, headers=self.headers, proxies=self.proxies) if proxies else requests.get(
            self.barrageUrl, headers=self.headers)
        self.filepath = os.path.join(
            self.savepath, self.title + '[' + self.author + ']' + '.xml')
        with open(self.filepath, 'wb') as f:
            f.write(res.content)

    def xml2ass(self):
        # 将xml文件转换为ass文件
        newName = self.filepath.replace("xml", "ass")
        tr(self.filepath, newName, 1920, 1080)
        os.remove(self.filepath)
        self.filepath = newName
        return True

    def downloadVideo(self):
        if not self.BBDownPath:
            return False
        subprocess.run(
            "{BBDown} {URL} --work-dir={saveDir}".format(
                BBDown=self.BBDownPath, URL=self.videoUrl, saveDir=self.savepath
            )
        )


d = Download(url='url', savepath=r"dir")
d.getHtml(proxies=False)
d.getMessage()
d.download(proxies=False)
d.xml2ass()
d.downloadVideo()
