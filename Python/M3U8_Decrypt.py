import os
import re
from enum import Enum

from Crypto.Cipher import AES

"""
本项目的路径格式仅适用于Windows，即反斜线，不适用于Linux
"""


def getKeyFromFile(fileName, dirPath):
    """
    从文件中读取密钥
    :param fileName: 密钥文件名
    :param dirPath: 密钥文件所在目录
    """
    for item in os.listdir(dirPath):
        if item == fileName:
            with open(os.path.join(dirPath, fileName), 'rb') as f:
                content = f.read()
            break
    return content


class Mode(Enum):
    """
    各种模式的常量
    """
    # 加密模式
    AES_128_CBC = 0  # AES-128-CBC加密模式，需要key参数和iv参数
    AES_128_ECB = 1  # AES-128-ECB加密模式，需要key参数


class Decrypt_AES128:
    def __init__(self, cryptoMode: Mode, m3u8Path, fileDir, outPath) -> None:
        self.crypto = cryptoMode  # 加密模式
        self.m3u8 = m3u8Path  # m3u8索引文件的链接
        self.inDir = fileDir  # 待解密文件所在的文件夹
        self.outDir = outPath  # 解密后文件的输出路径
        self.key = bytes()  # 目前来说，AES-128加密都需要key参数
        self.iv = bytes()  # AES-128-CBC需要额外的iv参数
        self.nameType = re.compile('')  # 命名格式
        self.init()  # 读取M3U8文件的内容
        self.menu()

    def menu(self):
        """
        菜单
        """
        print('菜单：')
        print('1. 解密单个文件')
        print('2. 解密全组文件')
        print('3. 清除原文件')
        print('4. 退出')
        choice = input('请输入您的选择：')
        if choice == '1':
            filePath = input('请输入需要解密的文件：')
            if self.decrypt_single(self.crypto, filePath):
                print('解密完成，已将文件保存至' + self.outDir)
                self.menu()
            else:
                print('解密失败')
                return False
        elif choice == '2':
            if self.decrypt(self.crypto):
                print('解密完成，已将文件保存至' + self.outDir)
                self.menu()
            else:
                print('解密失败')
                return False
        elif choice == '3':
            print('是否确认清除原文件：')
            choice = input('1. 确认\n2. 取消\n')
            if choice == '1':
                if self.removeSource():
                    print('清理完成')
                else:
                    print('清理失败')
                self.menu()
            elif choice == '2':
                print('输入有误，已取消')
                self.menu()
            else:
                print('命令输入错误，未清除原文件')
                self.menu()
        elif choice == '4':
            print('感谢使用')
            exit()
        else:
            print('输入有误，请重新输入')
            self.menu()

    def init(self):
        """
        读取M3U8文件的内容，初始化信息
        """
        if not (os.path.exists(self.inDir) and os.path.isdir(self.inDir)):  # 检查源文件路径
            return False
        if not os.path.exists(self.outDir):  # 检查保存路径
            os.makedirs(self.outDir)
        with open(self.m3u8, 'r', encoding='utf-8') as f:
            contents = [f.readline() for i in range(10)]  # 读取m3u8关键内容
        fileName = ''
        for line in range(len(contents)):
            if contents[line].startswith('#EXT-X-KEY'):
                key = re.findall(r'URI="(.*?)"', contents[line])[0]
                key = key[key.rfind('/') + 1:]  # 得到key参数
                # 对key参数的处理：若是16进制字符串，则转换为bytes，若是文件名，则以字节读取文件内容
                if len(key) == 32:
                    self.key = bytes.fromhex(key)
                elif key.endswith('.key'):  # 如果是文件，则读取其中的值
                    self.key = getKeyFromFile(key, self.inDir)
                iv = re.findall(r'IV=(.*?)$', contents[line])[0]  # 查找iv参数
                self.iv = bytes.fromhex(iv[2:]) if iv.startswith(
                    '0x') else bytes.fromhex(iv)  # 去除0x标记并转换为bytes
            elif contents[line].startswith('#EXTINF'):
                fileName = contents[line + 1].split('/')[-1]
                fileName.replace('\n', '')  # 得到命名格式
                break
        # 确定文件命名格式
        if re.match('^\d+$', fileName):
            self.nameType = re.compile('^\d+$')
        elif re.fullmatch('^\d+\.ts$', fileName):
            self.nameType = re.compile('^\d+\.ts$')
        elif re.fullmatch('^[a-zA-Z]+\d+$', fileName):
            self.nameType = re.compile('^[a-zA-Z]+\d+$')
        elif re.fullmatch('^[a-zA-Z]+\d+\.ts$', fileName):
            self.nameType = re.compile('^[a-zA-Z]+\d+\.ts$')

    def decrypt_single(self, mode, filePath):
        """
        只解密单个文件
        """
        with open(filePath, 'rb') as f:
            content = f.read()
        if mode == Mode.AES_128_CBC:
            cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        elif mode == Mode.AES_128_ECB:
            cryptor = AES.new(self.key, AES.MODE_ECB)
        else:
            return False
        decryptContent = cryptor.decrypt(content)
        with open(os.path.join(self.outDir, filePath.split('\\')[-1]), 'wb') as newFile:
            # 名称和源文件相同，但在输出文件夹下
            newFile.write(decryptContent)
        newFile.close()
        return True

    def decrypt(self, mode):
        """
        合并并解密
        """
        if mode == Mode.AES_128_CBC:
            cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        elif mode == Mode.AES_128_ECB:
            cryptor = AES.new(self.key, AES.MODE_ECB)
        else:
            return False
        # 将保存路径修改到文件级别
        if os.path.isdir(self.outDir):
            if not os.path.exists(self.outDir):
                os.mkdir(self.outDir)
            self.outDir = os.path.join(self.outDir, 'merge.ts')
        fileList = [f for f in os.listdir(
            self.inDir) if self.nameType.match(f)]  # 获取到文件
        # 按照数字部分升序排列，保证片段是逻辑连续的
        fileList.sort(key=lambda x: int(re.sub('[a-zA-Z]+', '', x)))
        newFile = open(self.outDir, 'wb')  # 新建一个合并后的文件
        for item in fileList:
            with open(os.path.join(self.inDir, item), 'rb') as file:
                content = cryptor.decrypt(file.read())
            newFile.write(content)
        newFile.close()
        return True

    def removeSource(self):
        try:
            for item in os.listdir(self.inDir):
                os.remove(os.path.join(self.inDir, item))
            os.removedirs(self.inDir)
            os.remove(self.m3u8)
            return True
        except:
            return False


start = Decrypt_AES128(cryptoMode=Mode.AES_128_CBC,
                       m3u8Path=r'', fileDir=r'', outPath=r'')
