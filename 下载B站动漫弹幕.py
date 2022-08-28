import os
import re
import shutil
import time

import requests

from xml2ass import Danmaku2ASS as tr


class Operate:
    def __init__(self, path, num):
        self.path = path
        self.num = num
        self.originPlayResX = 'PlayResX'
        self.changePlayResX = 'PlayResX:1920'
        self.originPlayResY = 'PlayResY'
        self.changePlayResY = 'PlayResY:1080'
        self.originDefaultFont = '方正准圆_GBK'
        self.changeFont = 'Microsoft YaHei UI'
        self.originFontSize = '22'
        self.changeFontSize = '40'

    def createExtraDir(self):
        # 创建Extra文件夹
        if not os.path.exists(os.path.join(self.path, 'Extra')):
            os.mkdir(os.path.join(self.path, 'Extra'))

    def renameSubtitle(self):
        # 重命名字幕文件(变为01.ass)
        self.createExtraDir()  # 检查下有没有Extra文件夹，没有就创建
        for j in os.listdir(self.path):
            if j.endswith('.ass') and 'Preview' not in j:
                name = j.split('.')[0]
                types = j.split('.')[-2]
                index = re.findall("[ \[]?\d{2}[ \]]?", j)[0].strip()
                index = re.sub('[\[\]]', '', index)
                if 'sc' in types or 'chs' in types or 'SC' in types or 'CHS' in types:
                    os.rename(os.path.join(path, j),
                              os.path.join(path, index + '.ass'))
                elif 'tc' in types or 'cht' in types or 'TC' in types or 'CHT' in types:
                    os.rename(os.path.join(path, j), os.path.join(
                        path, index + '_' + types + '.ass'))
                    shutil.move(os.path.join(path, index + '_' + types + '.ass'),
                                os.path.join(path, 'Extra'))  # 把繁体字幕挪到Extra中

    def renameVideo(self):
        # 重命名视频文件
        for j in os.listdir(self.path):
            if j.endswith('.mkv'):
                index = re.findall("[ \[]?\d{2}[ \]]?", j)[0].strip()
                index = re.sub('[\[\]]', '', index)
                os.rename(os.path.join(path, j),
                          os.path.join(path, index + '.mkv'))

    def xmlToAss(self, source):
        # 将xml文件转换为ass文件
        target = source.replace(".xml", "_Barrage.ass")
        tr(os.path.join(path, source), os.path.join(
            path, target), 1920, 1080)
        os.remove(os.path.join(path, source))

    def mergeSubtitleBarrage(self, changeFont=False, changeFontSize=False):
        for i in range(self.num):
            index = str(i + 1) if len(str(i + 1)) != 1 else '0' + str(i + 1)
            subtitle_name = index + '.ass'
            barrage_name = index + '_Barrage.ass'
            # 读取弹幕内容
            with open(os.path.join(self.path, barrage_name), 'r', encoding='utf-8', errors='ignore') as barrageContent:
                barrageContent = barrageContent.read()
            barrageContent = barrageContent.split('\n')
            # 读取字幕内容
            with open(os.path.join(self.path, subtitle_name), 'r', encoding='utf-8',
                      errors='ignore') as subtitleContent:
                subtitleContent = subtitleContent.read()
            subtitleContent = subtitleContent.split('\n')
            # 修改字幕文件中的设定参数
            for j in range(len(subtitleContent)):
                if 'PlayResX' in subtitleContent[j]:
                    subtitleContent[j] = self.changePlayResX
                elif 'PlayResY' in subtitleContent[j]:
                    subtitleContent[j] = self.changePlayResY
                # 下面这个是修改字幕字号的，通常来说字幕最小字号也要40以上才合适
                # elif 'Style: Default' in subtitleContent[j]:
                #     if changeFont:
                #         subtitleContent[j] = subtitleContent[j].replace(
                #             self.originDefaultFont, self.changeFont)
                #     if changeFontSize:
                #         subtitleContent[j] = subtitleContent[j].replace(
                #             self.originFontSize, self.changeFontSize)

            # 合并弹幕和字幕
            content = '\n'.join(subtitleContent) + '\n\n' + \
                      '\n'.join(barrageContent)
            with open(os.path.join(self.path, subtitle_name), 'w', encoding='utf-8',
                      errors='ignore') as newSubtitleContent:
                newSubtitleContent.write(content)
            # 删除弹幕文件
            os.remove(os.path.join(self.path, barrage_name))


class GetAss:
    def __init__(self, url, downloadPath):
        self.url = url
        self.downloadPath = downloadPath
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.proxies = {
            'http': 'http://127.0.0.1:10809',
            'https': 'http://127.0.0.1:10809'
        }

    def 批量下载(self, cidList):
        for j in range(len(cidList)):
            time.sleep(1)
            cid = cidList[j]
            url = f'https://comment.bilibili.com/{cid}.xml'
            res = requests.get(url, headers=self.headers, proxies=self.proxies)
            name = str(j + 1)
            if len(name) == 1:
                name = '0' + name
            with open(os.path.join(self.downloadPath, f'{name}.xml'), 'wb') as f:
                f.write(res.content)

    def 获取到全部cid(self, num, local=False):
        if local:
            with open(self.url, 'r', encoding='utf-8', errors='ignore') as f:
                res = f.read()
        else:
            res = requests.get(self.url, headers=self.headers,
                               proxies=self.proxies).text
        cid = re.findall(r'"cid":(.*?),', res)
        cid.remove('0')
        return cid[:num]


url = r"https://www.bilibili.com/bangumi/play/ep330669/"
path = r'E:\Videos\动漫\我的青春恋爱物语果然有问题\第3季'
num = 12
operate = Operate(path, num)
getass = GetAss(url, path)
operate.renameSubtitle()
# operate.renameVideo()
cidList = getass.获取到全部cid(num)  # 可以添加local=True参数，解析本地html
getass.批量下载(cidList)
# 将文件转换为ass
for j in os.listdir(path):
    if j.endswith('.xml'):
        operate.xmlToAss(j)
# 合并弹幕和字幕
operate.mergeSubtitleBarrage()
