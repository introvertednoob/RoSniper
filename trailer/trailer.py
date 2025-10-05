# Code for RoSniper's revamped trailer
# This is very unpolished and will probably stay that way indefinitely

import os
import time
import psutil
import pyautogui

gold = "\033[0;33m"
bold = "\033[1m"
end = "\033[0m"
rsexec = ".venv/bin/python3 rosniper.py"

def clear():
    os.system("clear")
    os.system("clear")

def open_tab():
    pyautogui.keyDown("command")
    pyautogui.press("t")
    pyautogui.keyUp("command")

def close_tab(enter=False):
    pyautogui.keyDown("command")
    pyautogui.press("w")
    pyautogui.keyUp("command")
    if enter:
        pyautogui.press("enter")

def intro():
    clear()
    print(f"{gold}{bold}Welcome to RoSniper! I'll be showing you some of the features we have to offer.{end}")
    time.sleep(1.5)
    print(f"First, let's snipe a player. How about my dearest friend?")
    time.sleep(1.5)
    open_tab()
    pyautogui.typewrite(rsexec)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite("awij128")
    pyautogui.press("enter")
    time.sleep(6)
    for proc in psutil.process_iter():
        if proc.name() == "RobloxPlayer":
            psutil.Process(proc.pid).kill()
    time.sleep(2)
    close_tab(True)

def monitoring():
    clear()
    time.sleep(0.3)
    print(f"You can {bold}monitor a user's status{end} instead of join-sniping them.")
    time.sleep(1.5)
    print("Just type /m in RoSniper!")
    time.sleep(2)
    open_tab()
    pyautogui.typewrite(rsexec)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite("/m")
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite("awij128")
    pyautogui.press("enter")
    time.sleep(3)
    close_tab(True)

def decline_first_server():
    clear()
    time.sleep(0.3)
    print(f"You can also {bold}decline the first server{end} that is found.")
    print("This can be useful when joining a streamer in an already full server.")
    time.sleep(2)
    print("Just type /df in RoSniper!")
    time.sleep(2)
    open_tab()
    pyautogui.typewrite(rsexec)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite("/df")
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.typewrite("awij128")
    pyautogui.press("enter")
    time.sleep(3)
    close_tab(True)

examples_NIM = [
    "    - Enter a username/Recent User ID to join-snipe that user",
    "    - Use -a[ID] to authenticate with that specific cookie",
    "    - Use -d or -m to enable Decline First Server/Monitoring-Only Mode respectively"
]
def non_interactive_mode():
    clear()
    time.sleep(0.3)
    print(f"We also offer {bold}a non-interactive mode!{end}")
    time.sleep(2)
    print(f"You can add command-line arguments to speedily access RoSniper.")
    time.sleep(2)
    print("\nFor example, you can:")
    for item in examples_NIM:
        print(item)
        time.sleep(0.5)
    time.sleep(2)
    print("\nBy the way, arguments can be stacked.")
    time.sleep(5)

def changelog_and_cmds():
    clear()
    time.sleep(0.3)
    print(f"To see what's changed after an update, {bold}type /changelog{end} in RoSniper.")
    time.sleep(2)
    print(f"Also, you can {bold}type /cmds{end} to see the command documentation.")
    time.sleep(3)

technical_stuff = [
    "Build of RoSniper displayed: v1.6.0",
    "Shot on macOS 26 Tahoe, no modifications made to RoSniper.py",
    "This trailer was made through a few hundred lines of Python",
    "    - (I kind of suck at video editing)"
]
def outro():
    clear()
    print(f"{gold}{bold}That's a brief overview on how RoSniper works!{end}")
    time.sleep(2)
    print("This project of mine has evolved over the past year, and I wanted to capture all the progress in a short trailer :D")
    time.sleep(2)
    print(f"\n{bold}Now, here's some cool technical stuff about this:{end}")
    for item in technical_stuff:
        print(item)
        time.sleep(0.5)
    time.sleep(2)
    print("\nBuilt by Aaron Wijesinghe with lots of love <3")

intro()
monitoring()
decline_first_server()
non_interactive_mode()
changelog_and_cmds()
outro()