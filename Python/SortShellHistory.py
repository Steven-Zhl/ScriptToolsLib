"""整理Shell的历史记录"""
from pathlib import Path
import os
from typing import Union
import platform
import argparse

BLOCKED_WORDS = []  # 屏蔽词，一旦包含任意屏蔽词，该记录即被删除
POSIX_PATH = False  # 是否将路径转换为POSIX格式，即将反斜杠转换为斜杠
ALLOW_REPEATED = False  # 是否允许重复的记录
VERBOSE = False  # 是否输出详细信息


def getHistoryPath() -> Union[Path, None]:
    """
    获取历史记录文件的路径
    :return: 
    """
    if platform.system() == "Windows":  # PowerShell
        historyFile = Path(
            os.getenv("USERPROFILE"),
            "AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt",
        )
        return historyFile if historyFile.exists() else None
    elif platform.system() == "Linux":  # Bash or Zsh
        if "bash" in os.getenv("SHELL"):
            historyFile = Path(os.getenv("HOME"), ".bash_history")
            return historyFile if historyFile.exists() else None
        elif "zsh" in os.getenv("SHELL"):
            historyFile = Path(os.getenv("HOME"), ".zsh_history")
            return historyFile if historyFile.exists() else None


def getHistory(file: Path) -> list[str]:
    if file.is_file() and file.exists():
        return file.read_text().split("\n")
    else:
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--block", nargs="+", help="Blocked words")
    parser.add_argument("-p", "--posix", action="store_true", help="Convert path to POSIX format")
    parser.add_argument("-r", "--repeat", action="store_true", help="Allow repeated records")
    parser.add_argument("-v", "--verbose", action="store_true", help="Output verbose information")
    args = parser.parse_args()
    if args.block:
        BLOCKED_WORDS = args.block
    if args.posix:
        POSIX_PATH = True
    if args.repeat:
        ALLOW_REPEATED = True
    if args.verbose:
        VERBOSE = True

    historyFile = getHistoryPath()
    if historyFile is None:
        print("History file not found.")
        exit(0)
    contents = getHistory(historyFile)
    if not contents:
        print("No history found.")
        exit(0)

    if VERBOSE:
        print("History file:".ljust(20), historyFile.as_posix())
        print("Blocked words:".ljust(20), BLOCKED_WORDS)
        print("Convert to POSIX:".ljust(20), POSIX_PATH)
        print("Allow repeated:".ljust(20), ALLOW_REPEATED)
        print("Verbose:".ljust(20), VERBOSE)
        print("History count:".ljust(20), len(contents))

        print("Sorting...")

    if not ALLOW_REPEATED:  # 去重
        contents = list(set(contents))
        if VERBOSE: print("After removing repeated records:".ljust(20), len(contents))
    if POSIX_PATH:
        contents = [line.replace("\\", "/") for line in contents]
    for word in BLOCKED_WORDS:  # 删除屏蔽词
        contents = [line for line in contents if word not in line]
    contents.sort()
    historyFile.write_text("\n".join(contents))
    if VERBOSE: print("Done.")
