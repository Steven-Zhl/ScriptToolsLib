from warnings import filterwarnings
from os import system
import process

supportApps = ["华为课程表"]  # 可选的软件，注意顺序最好不要改变
welcomeTips = ["Hello, YNU的同学", "这是一个帮助你将导出的课程表导入日程软件的脚本。",
               "其实说白了就是转换下格式。", "目前支持以下软件："]  # 提示消息
exitIndex = len(supportApps) + 1


def welcomePage(mode="normal"):
    """
    闲的无聊，做了一个欢迎界面
    mode==test->不显示各种提示信息（开发者界面）
    mode==normal->显示提示信息（用户的界面）
    """
    if mode == "normal":
        print("\n".join(welcomeTips))  # 打印提示信息
        for index in range(len(supportApps)):
            print("\t", index + 1, ".", supportApps[index])
        print(exitIndex, ". 退出")
    # 选择要进行的操作
    choice = int(input("\n请选择操作："))
    if choice == exitIndex:
        print("您已正常退出")
        exit(0)
    elif choice > len(supportApps):
        print("您的输入有误，请稍后重试")
        return
    else:
        if choice == 1:  # 华为课程表的操作代码
            sourceFile = process.askopenfilename(title="请输入教务导出的课程表路径：", fileType='.xlsx')
            time_1Week_Mon = process.get1WeekMondayDate("HWCalender")
            saveDir = process.askdirectory(title="请输入保存路径（文件夹名）：")

            calender = process.HWCalender(sourceFile, time_1Week_Mon, saveDir)
            calender.output(fileType="csv",charset='GBK', autoOpen=True)
            print("导出完成，即将自动打开")
            system("pause")


if __name__ == '__main__':
    filterwarnings('ignore')
    welcomePage()
