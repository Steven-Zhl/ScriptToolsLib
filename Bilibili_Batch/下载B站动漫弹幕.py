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
        self.indexPattern = [re.compile("\[\d{2}\]"), re.compile(
            " \d{2} "), re.compile("-\d{2}-")]  # 用于获取index的正则对象
        self.supportVideoType = ['.mkv', '.mp4', '.avi', '.flv', '.wmv']
        self.supportSubtitleType = ['.ass', '.sup']
        self.traditionalChinese = ['tc', 'cht', 'TC', 'CHT']  # 繁体中文的标识
        self.simpleChinese = ['sc', 'chs', 'SC', 'CHS']  # 简体中文的标识

    def createExtraDir(self):
        # 创建Extra文件夹
        if not os.path.exists(os.path.join(self.path, 'Extra')):
            os.mkdir(os.path.join(self.path, 'Extra'))

    def renameSubtitle(self):
        # 重命名字幕文件
        self.createExtraDir()  # 检查下有没有Extra文件夹，没有就创建
        for j in os.listdir(self.path):
            if j.endswith(tuple(self.supportSubtitleType)) and 'Preview' not in j:
                name, ext = ".".join(j.split('.')[:-1]), "."+j.split('.')[-1]
                # 判断字幕文件是简体还是繁体
                for key in self.traditionalChinese:
                    if key in name:
                        type = "Traditional"
                        break
                else:
                    type = "Simple"
                index = self.getIndex(j)
                # 判断完成后的操作：简体字幕重命名，繁体字幕移动到Extra中
                if type == 'Simple':
                    os.rename(os.path.join(path, j),
                              os.path.join(path, index + ext))
                elif type == 'Traditional':
                    os.rename(os.path.join(path, j), os.path.join(
                        path, index + '_' + types + ext))
                    shutil.move(os.path.join(path, index + '_' + types + ext),
                                os.path.join(path, 'Extra'))  # 把繁体字幕挪到Extra中

    def renameVideo(self):
        # 重命名视频文件
        for j in os.listdir(self.path):
            if j.endswith(tuple(self.supportVideoType)):
                index = self.getIndex(j)
                ext = j.split('.')[-1]
                os.rename(os.path.join(path, j),
                          os.path.join(path, index + "." + ext))

    def getIndex(self, name):
        for pattern in self.indexPattern:
            try:
                index = pattern.search(string=name).group()
                break
            except:
                continue
        index = re.sub('[- \[\]]', '', index) if '[' in index else index
        index = index.strip()
        return index

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

    def renameSingleBarrage(self):
        # 将Barrage.ass文件重命名为ass文件，作为默认挂载的字幕
        for j in os.listdir(self.path):
            if j.endswith('.ass') and "Barrage" in j:
                newName = j.replace("_Barrage", "")
                os.rename(os.path.join(path, j), os.path.join(path, newName))


class GetAss:
    def __init__(self, url, downloadPath):
        self.url = url
        self.downloadPath = downloadPath
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.proxies = {
            'http': 'http://127.0.0.1:port',
            'https': 'http://127.0.0.1:port'
        }  # 开启代理用，请自行分配端口

    def 批量下载(self, cidList, proxies=False):
        for j in range(len(cidList)):
            time.sleep(1)
            cid = cidList[j]
            url = f'https://comment.bilibili.com/{cid}.xml'
            res = requests.get(url, headers=self.headers, proxies=self.proxies) if proxies else requests.get(
                url, headers=self.headers)
            name = str(j + 1)
            if len(name) == 1:
                name = '0' + name
            with open(os.path.join(self.downloadPath, f'{name}.xml'), 'wb') as f:
                f.write(res.content)

    def 获取到全部cid(self, num, proxies=False):
        if proxies:
            res = requests.get(self.url, headers=self.headers,
                               proxies=self.proxies).text
        else:
            res = requests.get(self.url, headers=self.headers).text
        cid = re.findall(r'"cid":(.*?),', res)
        cid.remove('0')
        return cid[:num]


if __name__ == '__main__':
    哔哩哔哩链接 = r"https://www.bilibili.com/bangumi/play/ep510759/"  # 要下载的动漫的任意一集B站链接
    本地路径 = r'E:\Videos\动漫\夏日重现'  # 剧集及字幕所在的路径，请确保为一文件夹路径
    剧集数 = 25  # 剧集数，请保持本地与B站一致
    合并外挂ass字幕与弹幕 = True  # 只有字幕文件为单独的.ass文件，且想要合并字幕和弹幕到同一文件中时才为True，否则为False

    operate = Operate(本地路径, 剧集数)  # 请不要改动
    getass = GetAss(哔哩哔哩链接, 本地路径)  # 请不要改动
    operate.renameSubtitle()  # 重命名字幕文件，变为01.ass,02.ass这种形式
    operate.renameVideo()  # 重命名视频文件，变为01.mkv、02.mp4这种形式
    cidList = getass.获取到全部cid(剧集数)  # 请不要改动
    getass.批量下载(cidList)  # 请不要改动
    # 将文件转换为ass
    for j in os.listdir(path):
        if j.endswith('.xml'):
            operate.xmlToAss(j)
    if 合并外挂ass字幕与弹幕:
        operate.mergeSubtitleBarrage()
    else:
        operate.renameSingleBarrage()
