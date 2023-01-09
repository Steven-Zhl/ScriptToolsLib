import os
import re
from enum import Enum


# 错误类
class PathNotExistErr(FileExistsError):
    """输入的路径不存在"""

    def __init__(self, path):
        self.path = "您输入的路径'{}'不存在，请检查".format(path)

    def __str__(self):
        return repr(self.path)


class PathTypeErr(TypeError):
    """输入的路径不符合要求"""

    def __init__(self, path: str, require: any):
        actualType = 'Path' if os.path.isdir(path) else 'File'
        self.value = "您输入的路径'{}'与所需类型不符，要求为'{}'，实际为{}".format(
            path, require, actualType)

    def __str__(self):
        return repr(self.value)


class ChoiceRangeErr(KeyError):
    """选择超出范围"""

    def __init__(self, value: int, choiceRange: list):
        self.value = "您输入的选择'{}'超出范围，可用范围为'{}'".format(value, choiceRange)

    def __str__(self):
        return repr(self.value)


class Choice(Enum):
    menuFunction = ["字符串替换", "正则表达式替换", "添加自动序号", "退出"]
    replacePart = ["文件名", "扩展名", "文件名和扩展名"]


def ask(tips: str, content: list) -> dict:
    res = dict()
    print(tips)
    for i in range(len(content)):
        print("\t" + str(i + 1) + ". " + content[i])
        res[content[i]] = i + 1
    return res


class Rename:
    """重命名的操作类"""

    def __init__(self, dirPath: str) -> None:
        # 参数
        self.dirPath = ''  # 文件的根目录
        self.fileList = []  # 文件名称列表
        # dir存在性检查
        if not os.path.exists(dirPath):
            raise PathNotExistErr(dirPath)
        if not os.path.isdir(dirPath):
            raise PathTypeErr(dirPath, require='Path')
        self.dirPath = dirPath  # 被重命名文件的根目录
        self._refreshFileName() # 刷新self.fileList

    def mainloop(self):
        """mainloop，用于通常的，只修改单个Dir的操作类型"""
        while True:
            choiceIndex = self.menu()
            if choiceIndex == Choice.menuFunction.value.index('字符串替换')+1:
                self.replaceStr()
            elif choiceIndex == Choice.menuFunction.value.index('正则表达式替换')+1:
                self.replaceReg()
            elif choiceIndex == Choice.menuFunction.value.index('添加自动序号')+1:
                self.addAutoIndex()
            elif choiceIndex == Choice.menuFunction.value.index('退出')+1:
                exit(0)

    def _refreshFileName(self):
        """刷新fileList"""
        self.fileList = [i for i in os.listdir(self.dirPath)]  # 根目录下的文件
        self.fileList.sort()

    def _betchReplaceStr(self, originStr: str, newStr: str, rangeIndex: int) -> int:
        """重命名功能函数，被调用"""
        rangeType = Choice.replacePart.value[rangeIndex - 1]  # 获取范围的文字表述
        nameChange = []  # 记录旧文件名和新文件名
        # 获取新旧文件名对应
        for originName in self.fileList:
            newName = originName
            if rangeType == '文件名':
                name, ext = os.path.splitext(originName)
                newName = name.replace(originStr, newStr) + ext
            elif rangeType == '扩展名':
                name, ext = os.path.splitext(originName)
                newName = name + ext.replace(originStr, newStr)
            elif rangeType == '文件名和扩展名':
                newName = originName.replace(originStr, newStr)
            if originName != newName:
                nameChange.append({'origin': originName, 'new': newName})
        # 执行重命名
        try:
            for j in nameChange:
                os.rename(os.path.join(self.dirPath, j['origin']), os.path.join(
                    self.dirPath, j['new']))
        except PermissionError or FileNotFoundError or FileExistsError as e:
            raise e
        finally:
            self._refreshFileName()
            return len(nameChange)

    def _betchReplaceReg(self, target: re.compile, newStr: str):
        """重命名功能函数，被调用"""
        print("正在建设中...")
        pass

    def menu(self):
        choiceList = ask("功能:", Choice.menuFunction.value)
        choiceIndex = eval(input("请选择:"))
        if not isinstance(choiceIndex, int):
            raise TypeError(choiceIndex)
        if choiceIndex < 1 or choiceIndex > len(choiceList):
            raise ChoiceRangeErr(choiceIndex, [1, len(choiceList)])
        return choiceIndex

    def replaceStr(self, choice=None):
        # 是否已经由外部指定了choice
        if not choice:
            choiceList = ask("被替换部分:", Choice.replacePart.value)
            choiceIndex = eval(input("请选择:"))
            # 检查choiceIndex是否合法
            if not isinstance(choiceIndex, int):
                raise TypeError(choiceIndex)
            if choiceIndex < 1 or choiceIndex > len(choiceList):
                raise ChoiceRangeErr(choiceIndex, [1, len(choiceList)])
        else:
            choiceIndex = Choice.replacePart.value.index(choice)+1
        originStr = input("输入被替换字符串:")
        # 检查旧字符串是否确实存在
        if not [i for i in self.fileList if originStr in i]:
            print('在文件中不包含该字符串，请检查后重试')
            return
        newStr = input("输入新字符串:")
        # 检查新字符串是否合法
        if re.findall('[\/\?*:<>|"]', newStr):
            print('在新字符串中包括了非法字符，请检查后重试')
            return
        # 执行重命名
        modifyLineNum = self._betchReplaceStr(originStr, newStr, choiceIndex)
        print('执行完成，有{}个文件被修改'.format(modifyLineNum))

    def replaceReg(self):
        print("正在建设中...")
        pass

    def addAutoIndex(self):
        print("正在建设中...")
        pass


if __name__ == "__main__":
    mode = 'betch'
    if mode == 'betch':
        while True:
            dirPath = input("请输入文件根目录:")
            rename = Rename(dirPath=dirPath)
            rename.replaceStr(choice='文件名和扩展名')
    elif mode == 'simple':
        dirPath=input("请输入文件根目录:")
        rename=Rename(dirPath=dirPath)
        rename.mainloop()