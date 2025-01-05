## Ever wanted to join someone instantly on Roblox? (I have!)
This has allowed for me to get into people's servers *way faster*. It's helped me get certain items that require you to join famous people. And I'm sharing a (hopefully more polished) version of that program.

## Current Features:
- Snipe users you recently tried to join, for easier access to them
- Most of the program is customizable using commands or by modifying config.py
- Check for multiple user statuses at the same time

## How does RoSniper work?
RoSniper uses Roblox's Presence API to check if they are online.
If so, then it will attempt to join that user.

## How do I build this from source?
There is a build script in ./build/ that can be used to build RoSniper for macOS.
This creates an executable that anyone (even if they don't have Python) can run.
Clone this repository and run it, or just run the source code itself.

Tested on macOS 15 with Python 3.13 and 3.13.1! It likely also works on previous versions of macOS/Python 3.
Windows support is unlikely due to launching Roblox with deeplinking being MUCH slower on Windows than on macOS.