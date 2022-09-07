import os.path
import re

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

    def getHtml(self, proxies=False):
        # 获取html内容
        res = requests.get(self.videoUrl, headers=self.headers, proxies=self.proxies) if proxies else requests.get(
            self.videoUrl, headers=self.headers)
        self.html = res.text

    def getMessage(self):
        soup = BS(self.html, 'html.parser')
        self.title = str(soup.find(name="title").contents[0])
        self.title = self.title.replace('_哔哩哔哩_bilibili', '').strip()
        self.cid = re.findall(r'"cid":(.*?),', self.html)[0]
        if soup.find(class_="normal-members-container"):
            members = soup.find(
                class_="normal-members-container").find_all(class_="upname")
            self.author = "; ".join([partner.text for partner in members])
        else:
            self.author = (soup.find_all(class_='name')[
                           0]).find_next("a").contents[0]
            self.author = self.author.replace('\n', '').strip()
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


d = Download(url='url',
             savepath=r"dir")
d.getHtml(proxies=False)
d.getMessage()
d.download()
d.xml2ass()
