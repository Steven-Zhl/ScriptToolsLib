import time
import pymysql as DB
import csv
import re
import threading

MySQL_Root = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'pictures',
}
MySQL_Admin = {
    'host': 'localhost',
    'port': 3306,
    'user': 'Admin',
    'password': '',
    'database': 'pictures',
}
CSV_Path = ""


def main():
    db = DB.connect(**MySQL_Root)
    cursor = db.cursor()
    itemList = []
    with open(CSV_Path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        content = [row for row in reader]
        header = content.pop(0)
        header[0] = 'id'  # 这个是编码问题
        content = [dict(zip(header, row)) for row in content]
    # 格式化content
    for item in content:
        if item['type'] == 'Illustration':
            tmp = {'Title': item['title'].replace("'", r"\'"),
                   'Source': 'Pixiv',
                   'Source_ID': item['id'],
                   'Source_ID_Index': [str(i) for i in range(int(item['page']))],
                   'Painter': item['user'],
                   'Painter_ID': item['userId'],
                   'Age_Level': '家长指导级' if item['xRestrict'] == 'AllAges' else 'R-18',
                   'Width': item['width'],
                   'Height': item['height'],
                   'Identity': '插画'}
            tags = item['tags_transl'].split(',')
            tags = [tag for tag in tags if not re.search('[^\d]+[1-9]+0+[^\d]+', tag)]  # 将“XXXX收藏”之类的tags删除
            tags = [tag.replace("'", r"\'") for tag in tags]  # 将定界符转义
            tmp['Tags'] = tags
            itemList.append(tmp)

    # 准备对象写入数据库
    for item in itemList[84:]:
        # 先检查是否有该作者
        cursor.execute(
            "SELECT * FROM author WHERE Pixiv_ID = %s" % item['Painter_ID'])
        existAuthor = cursor.fetchone()
        if not existAuthor:  # 不存在则插入作者信息
            cursor.execute(
                "INSERT INTO author(Name,Identity,Pixiv_ID) VALUES ('%s','画师',%s)" % (
                    item['Painter'], item['Painter_ID']))
            db.commit()
        else:  # 存在，则将Painter插入进Name_Others字段，并更新item['Painter']为实际表中存储的名字
            cursor.execute(
                "SELECT Name_Others FROM author WHERE Pixiv_ID = %s" % item['Painter_ID'])
            Name_Other = cursor.fetchone()[0]
            if Name_Other is None:
                Name_Other = item['Painter']
            elif item['Painter'] not in Name_Other:
                Name_Other = ",".join([Name_Other, item['Painter']])
            cursor.execute(
                "UPDATE author SET Name_Others = '%s' WHERE Pixiv_ID = %s" % (Name_Other, item['Painter_ID']))
            db.commit()
            cursor.execute("SELECT Name FROM author WHERE Pixiv_ID = %s" % item['Painter_ID'])
            item['Painter'] = cursor.fetchone()[0]
        # 将文件信息写入illustration表中，并添加对应的tags
        cursor.execute("SELECT ID FROM pictures.author WHERE Pixiv_ID=%s" % item['Painter_ID'])
        authorID = cursor.fetchone()[0]  # 注意，illustration表中的Painter_ID字段不是Pixiv账号，而是author表的表内ID
        for i in item['Source_ID_Index']:
            cursor.execute(
                "INSERT INTO illustration SET Title = '%s', Source = '%s', Source_ID = '%s', Source_ID_Index = %s, Painter = '%s', Painter_ID = %s, Age_Level = '%s', Width = %s, Height = %s" % (
                    item['Title'],
                    item['Source'],
                    item['Source_ID'],
                    i,
                    item['Painter'],
                    authorID,
                    item['Age_Level'],
                    item['Width'],
                    item['Height']
                )
            )
            db.commit()
            # 添加tags
            for tag in item['Tags']:
                cursor.execute(
                    "INSERT INTO tags_illustration(Source, Source_ID, Source_ID_Index, Painter, Painter_ID, Identity, Tag) VALUES ('%s', '%s', %s, '%s',%s, '%s', '%s')" % (
                        item['Source'],
                        item['Source_ID'],
                        i,
                        item['Painter'],
                        authorID,
                        item['Identity'],
                        tag
                    ))
                db.commit()


def showProcess(task_num: int, barLength=60):
    last_num = 0
    while True:
        db = DB.connect(**MySQL_Admin)
        cursor = db.cursor()
        cursor.execute("SELECT Count(*) FROM pictures.illustration")
        curr_num = int(cursor.fetchone()[0]) + 1
        if last_num != curr_num:
            # 绘制进度条
            percent = curr_num / task_num
            pic_block_num = int(percent * barLength)
            print("Pictures:" + "#" * pic_block_num + "_" * (barLength - pic_block_num),
                  "{:.2f}".format(percent * 100),
                  str(curr_num) + "/" + str(task_num))
            # 更新数据
            last_num = curr_num
        else:
            print("任务执行完成")
            return
        db.close()
        time.sleep(1)


class MainThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        main()


class ShowProcess(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        showProcess(930)


if __name__ == "__main__":
    mode = 'batch'
    if mode == 'batch':
        mainProcess = MainThread(1, 'MainProcess', 1)
        countProcess = ShowProcess(2, 'ShowProcess', 2)
        mainProcess.start()
        countProcess.start()
    elif mode == 'debug':
        main()
    else:  # test
        showProcess(930)
