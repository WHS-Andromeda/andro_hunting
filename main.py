# main.py
from modules.run import multiRun
from modules.file_handler.text import readText


def main():
    al = readText("applist.txt")
    multiRun(al)


if __name__ == "__main__":
    main()
