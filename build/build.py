import os
import platform

class ansi:
    BROWN = "\033[0;33m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def clear():
    os.system("clear || cls")

if platform.system() == "Darwin":
    def build():
        clear()
        print(f"{ansi.BROWN}[Option 2 - Build RoSniper]{ansi.END}")
        print("Here are the requirements to build RoSniper for macOS:")
        print("    - RoSniper.py in the directory of the build script")
        print("    - AppIcon.icns, launcher.py, and Info.plist in ./Resources/")
        print("    - Dependencies: pyinstaller==6.13.0, pyperclip==1.9.0, and requests==2.32.3")

        if os.path.exists("../RoSniper.py"):
            RoSniperPath = "../RoSniper.py"
        elif os.path.exists("./RoSniper.py"):
            RoSniperPath = "./RoSniper.py"
        else:
            input("RoSniper.py wasn't found. ")
            return

        listedVersion = open(RoSniperPath, "r").read().split("version = \"")[1].split("\"")[0]
        print(f"\nSOURCE RoSniper Version: {listedVersion}")
        version = input("Set the EXECUTABLE RoSniper Version (press ENTER for same version): ").strip()
        if version == "":
            version = listedVersion
        modifiedPLIST = open("./Resources/Info.plist", "r").read().replace("0.0.0", version)
        modifiedRoSniper = open(RoSniperPath, "r").read().replace(f"version = \"{listedVersion}\"", f"version = \"{version}\"")
        open("./Resources/RoSniper.py", "w").write(modifiedRoSniper)

        if not os.path.exists('./Resources/launcher') and os.path.exists("./Resources/launcher.py"):
            os.system("pyinstaller ./Resources/launcher.py")
            os.system("cp ./dist/launcher/launcher ./Resources/")
            os.system("rm -rf build dist *.spec")
        
        os.system("pyinstaller --windowed ./Resources/RoSniper.py --icon ./Resources/AppIcon.icns")
        os.system("cp -r dist/RoSniper.app .")
        os.system("cp ./Resources/launcher RoSniper.app/Contents/MacOS/")
        open("./RoSniper.app/Contents/Info.plist", "w").write(modifiedPLIST)
        os.system("rm -rf build dist *.spec ./Resources/RoSniper.py")

    def transfer_changelog(confirmation=True):
        clear()
        print(f"{ansi.BROWN}[Option 3 - Inject changelog into RoSniper]{ansi.END}")
        if not os.path.exists("RoSniper.app"):
            input("RoSniper.app wasn't found. Build it using Option 2. ")
            return

        if os.path.exists("../changelog.txt"):
            print("changelog.txt was found in the parent directory.")
            os.system("cp ../changelog.txt RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./changelog.txt"):
            print("changelog.txt was found in this directory.")
            os.system("cp ../changelog.txt RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./Resources/changelog.txt"):
            print("changelog.txt was found in the Resources folder.")
            os.system("cp ../changelog.txt RoSniper.app/Contents/Frameworks/")
        else:
            input("changelog.txt wasn't found. ")
            return

        if confirmation == True:
            input("changelog.txt was injected into RoSniper.app. ")

    def transfer_cmd_docs(confirmation=True):
        clear()
        print(f"{ansi.BROWN}[Option 4 - Inject changelog into RoSniper]{ansi.END}")
        if not os.path.exists("RoSniper.app"):
            input("RoSniper.app wasn't found. Build it using Option 2. ")
            return

        if os.path.exists("../commands.txt"):
            print("commands.txt was found in the parent directory.")
            os.system("cp ../commands.txt RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./commands.txt"):
            print("commands.txt was found in this directory.")
            os.system("cp ../commands.txt RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./Resources/commands.txt"):
            print("commands.txt was found in the Resources folder.")
            os.system("cp ../commands.txt RoSniper.app/Contents/Frameworks/")
        else:
            input("commands.txt wasn't found. ")
            return

        if confirmation == True:
            input("commands.txt was injected into RoSniper.app. ")

    def transfer_config(confirmation=True):
        clear()
        print(f"{ansi.BROWN}[Option 5 - Inject config.py into RoSniper]{ansi.END}")
        if not os.path.exists("RoSniper.app"):
            input("RoSniper.app wasn't found. Build it using Option 2. ")
            return

        if os.path.exists("../config.py"):
            print("config.py was found in the parent directory.")
            os.system("cp ../config.py RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./config.py"):
            print("config.py was found in this directory.")
            os.system("cp ../config.py RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./Resources/config.py"):
            print("config.py was found in the Resources folder.")
            os.system("cp ../config.py RoSniper.app/Contents/Frameworks/")
        else:
            input("config.py wasn't found. ")
            return

        if confirmation == True:
            input("config.py was injected into RoSniper.app. ")

    def transfer_to_applications(confirmation=True):
        clear()
        print(f"{ansi.BROWN}[Option 6 - Transfer RoSniper to /Applications]{ansi.END}")
        if os.path.exists("/Applications/RoSniper.app"):
            os.system("rm -rf /Applications/RoSniper.app")
        os.system("mv RoSniper.app /Applications/")
        if confirmation == True:
            input("RoSniper.app was moved to the Applications folder. ")

    def delete_from_applications():
        clear()
        print(f"{ansi.BROWN}[Option 7 - Delete RoSniper from /Applications]{ansi.END}")
        if os.path.exists("/Applications/RoSniper.app"):
            os.system("rm -rf /Applications/RoSniper.app")
            input("RoSniper.app was deleted from the Applications folder. ")
        else:
            input("RoSniper.app wasn't found in the Applications folder. ")

    while True:
        clear()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        print(f"{ansi.BROWN}[RoSniper Build Tool]{ansi.END}")
        print(f"  {ansi.BOLD}[1] Install RoSniper from source (Options 2, 3, 4, and 5 combined){ansi.END}")
        print("  [2] Build RoSniper")
        print("  [3] Inject an existing changelog.txt into RoSniper.app")
        print("  [4] Inject an existing changelog.txt into RoSniper.app")
        print("  [5] Inject an existing config.py into RoSniper.app")
        print("  [6] Transfer RoSniper to /Applications")
        print("  [7] Delete RoSniper from /Applications")
        print("  [8] Exit")

        option = input("\nSelect an option: ").strip()
        if not option.isnumeric() and not option in ["1", "2", "3", "4", "5", "6", "7"]:
            input("\nInvalid option. ")
            continue
        else:
            option = int(option)

        match option:
            case 1:
                build()
                transfer_changelog(confirmation=False)
                transfer_config(confirmation=False)
                transfer_cmd_docs(confirmation=False)
                transfer_to_applications(confirmation=False)
            case 2:
                build()
            case 3:
                transfer_changelog()
            case 4:
                transfer_cmd_docs()
            case 5:
                transfer_config()
            case 6:
                transfer_to_applications()
            case 7:
                delete_from_applications()
            case 8:
                exit()
elif platform.system() == "Windows":
    input("The build script is not available for Windows at this time. ")
elif platform.system() == "Linux":
    input("The build script is not available for Linux at this time. ")
