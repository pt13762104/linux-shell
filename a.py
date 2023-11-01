from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import clear
from datetime import datetime
from time import localtime, strftime
import os, glob


def expand_path(pth):
    _res = []
    for i in pth:
        _res.extend(glob.glob(i))
        if len(glob.glob(i)) == 0:
            print("Path " + i + " not found.")
    _res = list(set(_res))
    res = {"files": [], "dirs": []}
    for j in _res:
        if not os.path.isdir(j):
            res["files"].append(j)
        else:
            res["dirs"].append(j)
    return [res, _res]


history = InMemoryHistory()
session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())
start_time = datetime.now()
while True:
    cmd = session.prompt(os.getcwd() + "$ ").split()
    if not len(cmd):
        continue
    _cmd = cmd[0]
    args = cmd[1:]
    if _cmd == "ls":
        paths = expand_path(args)
        if len(args) == 0:
            res = glob.glob("*")
            for i in res:
                print(i, end=" ")
            print()
        else:
            for i in paths[0]["files"]:
                print(i, end=" ")
            if len(paths[0]["files"]):
                print()
            for i in paths[0]["dirs"]:
                rs = os.listdir(i)
                print(i + ":")
                for j in rs:
                    print(j, end=" ")
                print()
    elif _cmd == "exit":
        break
    elif _cmd == "cd":
        paths = expand_path(args)
        if len(paths[0]["dirs"]) == 0 and len(args) != 0:
            print("Command " + _cmd + " called with no directory.")
            continue
        paths = paths[1]
        if len(args) == 0:
            os.chdir(os.path.expanduser("~"))
        elif len(paths) == 1:
            os.chdir(paths[0])
        else:
            print("Command " + _cmd + " called with too many arguments.")
    elif _cmd == "cat":
        paths = expand_path(args)
        if len(paths) == 1:
            continue
        if len(paths[0]["dirs"]) > 0:
            print("Command " + _cmd + " called with directories.")
            continue
        if len(paths[0]["files"]) == 0:
            print("Command " + _cmd + " called with no file.")
            continue
        for i in paths[0]["files"]:
            f = open(i, "r")
            print(f.read(), end="")
    elif _cmd == "help":
        print(
            """This is a simulation of a Linux terminal.
Commands:
- cat <files...> : print <files...>.
- ls <files/dirs...> : list the content of <files/dirs...>.
- cd <dir> : change the working directory to <dir>.
- exit: exit the shell.
- history: show the command history.
- clear: clears the screen."""
        )
    elif _cmd == "history":
        for j in history.get_strings():
            print(j)
    elif _cmd == "clear":
        clear()
    elif _cmd == "uptime":
        td = datetime.now() - start_time
        hours = td.seconds // 3600
        mins = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        print(f"{td.days} days, {hours} hours, {mins} minutes, {seconds} seconds")
    elif _cmd == "date":
        print(strftime("%a, %d %b %Y %H:%M:%S %z", localtime()))
    else:
        print("Command " + _cmd + " not found.")
