"""整理PowerShell的历史记录"""
from pathlib import Path
import os

HISTORY = os.path.join(
    os.getenv("USERPROFILE"),
    "AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt",
)
BLOCKED_WORDS = []  # 屏蔽词，一旦包含任意屏蔽词，该记录即被删除

if __name__ == "__main__":
    # 1. 读取历史记录
    try:
        with open(HISTORY, "r") as f:
            content: list[str] = f.readlines()
    except PermissionError as e:
        print(f"Permission Error to read history file '{HISTORY.name}'.")
        exit(-1)
    # 2. 去重
    content = list(set(content))
    # 3. 移除屏蔽词
    for word in BLOCKED_WORDS:
        content = [line for line in content if word not in line]
    # 4. 排序
    content.sort()
    # 5. 保存
    with open(HISTORY, "w") as f:
        f.writelines(content)
