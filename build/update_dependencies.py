"""
RoSniper Update Dependency Tool (used since v1.5.1)
I am using this script to update dependencies for both the macOS and Windows official releases.

DISCLAIMER: DO NOT EXPECT THIS SCRIPT TO BE STABLE, NOR EXPECT IT TO WORK ON YOUR MACHINE.
"""

import os
import getpass

def clear():
    for i in range(2):
        os.system("clear")

def update_macos():
    print("[Updating dependencies for macOS...]")
    print("> .venv/bin/pip3 install -r requirements.txt --upgrade")
    os.system(".venv/bin/pip3 install -r requirements.txt --upgrade")

def update_windows():
    print("[Updating dependencies for Windows...]")
    print(f"> WINEDEBUG=-all wine C:/Users/{getpass.getuser()}/appdata/local/programs/python/python314/scripts/pip.exe install -r requirements.txt --upgrade")
    os.system(f"WINEDEBUG=-all wine C:/Users/{getpass.getuser()}/appdata/local/programs/python/python314/scripts/pip.exe install -r requirements.txt --upgrade")

os.chdir(f"{os.path.dirname(__file__)}/..")
clear()
print("[Dependency Updater]")
op = input("Update dependencies for [W]indows (through WINE), [m]acOS, or [b]oth? ").lower().strip()
clear()
if op == "w":
    update_windows()
elif op == "m":
    update_macos()
elif op == "b":
    update_macos()
    clear()
    update_windows()
else:
    input("This OS isn't supported by the RoSniper dependency updater. ")
    exit()

clear()
print("[Success!]")
input("Successfully updated dependencies! ")