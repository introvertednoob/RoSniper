# Code for RoSniper's revamped trailer
# Tested on RoSniper v1.6.0 (no modifications made)

import os
import time
import psutil
import pyautogui

gold = "\033[0;33m"
bold = "\033[1m"
end = "\033[0m"
rsexec = ".venv/bin/python3 rosniper.py"

def type_and_enter(word, secs=0):
    pyautogui.typewrite(word)
    pyautogui.press("enter")
    time.sleep(secs)

def clear():
    for i in range(2):
        os.system("clear")

def print_wait(msg, secs=0):
    print(msg)
    time.sleep(secs)

def open_tab():
    pyautogui.keyDown("command")
    pyautogui.press("t")
    pyautogui.keyUp("command")

def close_tab():
    pyautogui.keyDown("command")
    pyautogui.press("w")
    pyautogui.keyUp("command")

def intro():
    clear()
    print_wait(f"{gold}{bold}Welcome to RoSniper! I'll be showing you some of the features we have to offer.{end}", 1.5)
    print_wait(f"First, let's snipe a player. How about my dearest friend?", 1.5)
    open_tab()
    type_and_enter(rsexec, 1)
    type_and_enter("awij128", 6)
    for proc in psutil.process_iter():
        if proc.name() == "RobloxPlayer":
            psutil.Process(proc.pid).kill()
    time.sleep(2)
    close_tab()

def monitoring():
    clear()
    time.sleep(0.3)
    print_wait(f"You can {bold}monitor a user's status{end} instead of join-sniping them.", 1.5)
    print_wait("Just type /m in RoSniper!", 2)
    open_tab()
    type_and_enter(rsexec, 1)
    type_and_enter("/m", 1)
    type_and_enter("awij128", 3)
    close_tab()

def decline_first_server():
    clear()
    time.sleep(0.3)
    print(f"You can also {bold}decline the first server{end} that is found.")
    print_wait("This can be useful when joining a streamer in an already full server.", 2)
    print_wait("Just type /df in RoSniper!", 2)
    open_tab()
    type_and_enter(rsexec, 1)
    type_and_enter("/df", 1)
    type_and_enter("awij128", 3)
    close_tab()

examples_NIM = [
    "    - Enter a username/Recent User ID to join-snipe that user",
    "    - Use -a[ID] to authenticate with that specific cookie",
    "    - Use -d or -m to enable Decline First Server/Monitoring-Only Mode respectively"
]
def non_interactive_mode():
    clear()
    time.sleep(0.3)
    print_wait(f"We also offer {bold}a non-interactive mode!{end}", 2)
    print_wait(f"You can add command-line arguments to speedily access RoSniper.", 2)
    print("\nFor example, you can:")
    for item in examples_NIM:
        print_wait(item, 0.5)
    time.sleep(2)
    print_wait("\nBy the way, arguments can be stacked.", 5)

def changelog_and_cmds():
    clear()
    time.sleep(0.3)
    print_wait(f"To see what's changed after an update, {bold}type /changelog{end} in RoSniper.", 2)
    print_wait(f"Also, you can {bold}type /cmds{end} to see the command documentation.", 3)

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
    print_wait("This project of mine has evolved over the past year, and I wanted to capture all the progress in a short trailer :D", 2)
    print(f"\n{bold}Now, here's some cool technical stuff about this:{end}")
    for item in technical_stuff:
        print_wait(item, 0.5)
    time.sleep(2)
    print("\nBuilt by Aaron Wijesinghe with lots of love <3")

intro()
monitoring()
decline_first_server()
non_interactive_mode()
changelog_and_cmds()
outro()