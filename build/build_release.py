"""
RoSniper Release Build Tool (used since v1.1.0)
I'm open sourcing this component to be transparent on how the pre-built binaries are created.

DISCLAIMER: THIS BUILD SCRIPT MAY CHANGE AT ANY TIME.
DO NOT EXPECT THIS TO BE STABLE, NOR EXPECT IT TO WORK ON YOUR MACHINE.
For a more stable and consumer-friendly build script, see build.py!
"""

import os
import shutil
import getpass
import zipfile
import platform

brown = "\033[0;33m"
bold = "\033[1m"
end = "\033[0m"

op = platform.system()
def clear():
    os.system("clear;clear" if op == "Darwin" else "cls")

if not op == "Darwin":
    clear()
    input("The macOS + Windows (through WINE) build script is only available on macOS. ")
    exit()

def build(ops):
    clear()
    print(f"{brown}[Building RoSniper for platform '{ops}']{end}")
    if os.path.exists("../RoSniper.py"):
        RoSniperPath = "../RoSniper.py"
    elif os.path.exists("./RoSniper.py"):
        RoSniperPath = "./RoSniper.py"
    else:
        input("RoSniper.py wasn't found. ")
        return

    version = open(RoSniperPath, "r").read().split("version = \"")[1].split("\"")[0]
    modifiedPLIST = open("./Resources/Info.plist", "r").read().replace("0.0.0", version)

    if ops == "Windows":
        if os.path.exists(f"./RoSniper-Windows/"):
            shutil.rmtree("./RoSniper-Windows/")

        os.mkdir(f"./RoSniper-Windows/")
        os.system(f"wine C:/Users/{getpass.getuser()}/appdata/local/programs/python/python313/scripts/pyinstaller.exe {RoSniperPath} --icon ./Resources/AppIcon.ico")
        os.system(f"cp -r ./dist/RoSniper/_internal/ ./RoSniper-Windows/_internal")
        os.system(f"cp ./dist/RoSniper/RoSniper.exe ./RoSniper-Windows/RoSniper.exe")
    elif ops == "Darwin":
        if not os.path.exists("./Resources/launcher") and os.path.exists("./Resources/launcher.py"):
            os.system("pyinstaller ./Resources/launcher.py")
            os.system("cp ./dist/launcher/launcher ./Resources/")
            os.system("rm -rf build dist *.spec")

        os.system(f"pyinstaller --windowed {RoSniperPath} --icon ./Resources/AppIcon.icns")
        os.system("cp -r ./dist/RoSniper.app ./RoSniper.app")
        os.system("cp ./Resources/launcher ./RoSniper.app/Contents/MacOS/")
        for delete in os.listdir("./RoSniper.app/Contents/Resources/"):
            if delete != "AppIcon.icns":
                os.system(f"rm -rf ./RoSniper.app/Contents/Resources/{delete}")
        open("./RoSniper.app/Contents/Info.plist", "w").write(modifiedPLIST)
    os.system("rm -rf build dist *.spec")

def transfer_assets(ops):
    if os.path.exists(f"../assets"):
        path = f"../assets"
    elif os.path.exists(f"./assets"):
        path = f"./assets"
    elif os.path.exists(f"./Resources/assets"):
        path = f"./Resources/assets"
    else:
        return

    if ops == "Windows":
        if not os.path.exists("./RoSniper-Windows/_internal/assets/"):
            os.mkdir("./RoSniper-Windows/_internal/assets/")
    elif ops == "Darwin":
        if not os.path.exists("./RoSniper.app/Contents/Frameworks/assets/"):
            os.mkdir("./RoSniper.app/Contents/Frameworks/assets/")

    os.system(f"cp -r {path}/* {"./RoSniper-Windows/_internal/assets/" if ops == "Windows" else "./RoSniper.app/Contents/Frameworks/assets"}")

def build_darwin():
    build("Darwin")
    transfer_assets("Darwin")

def build_windows():
    build("Windows")
    transfer_assets("Windows")

    with zipfile.ZipFile("RoSniper-windows.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("./RoSniper-Windows"):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, "./RoSniper-Windows")
                zipf.write(full_path, rel_path)

    if os.path.exists("./RoSniper-Windows/"):
        shutil.rmtree("./RoSniper-Windows/")

while True:
    clear()
    os.chdir(os.path.dirname(__file__))

    print(f"{brown}[RoSniper Build Tool]{end}")
    print(f"{bold}[1] Build RoSniper for macOS + Windows (through WINE){end}")
    print(f"[2] Build RoSniper for macOS")
    print(f"[3] Build RoSniper for Windows (through WINE)")
    print(f"[4] Exit")

    option = input("\nSelect an option: ").strip()
    if not option.isnumeric() or not option in ["1", "2", "3", "4"]:
        input("Invalid option. ")
        continue
    else:
        option = int(option)

    match option:
        case 1:
            build_darwin()
            build_windows()
        case 2:
            build_darwin()
        case 3:
            build_windows()
        case 4:
            exit()