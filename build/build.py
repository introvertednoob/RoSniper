import os
import platform

brown = "\033[0;33m"
bold = "\033[1m"
faint = "\033[2m"
end = "\033[0m"

def clear():
    os.system("clear || cls")

if platform.system() == "Darwin":
    def build():
        clear()
        print(f"{brown}[Option 2 - Build RoSniper]{end}")
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
        print(f"{brown}[Option 3 - Inject changelog into RoSniper]{end}")

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
        print(f"{brown}[Option 4 - Inject changelog into RoSniper]{end}")

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
        print(f"{brown}[Option 5 - Inject config.json into RoSniper]{end}")

        if os.path.exists("../config.json"):
            print("config.json was found in the parent directory.")
            os.system("cp ../config.json RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./config.json"):
            print("config.json was found in this directory.")
            os.system("cp ../config.json RoSniper.app/Contents/Frameworks/")
        elif os.path.exists("./Resources/config.json"):
            print("config.json was found in the Resources folder.")
            os.system("cp ../config.json RoSniper.app/Contents/Frameworks/")
        else:
            input("config.json wasn't found. ")
            return

        if confirmation == True:
            input("config.json was injected into RoSniper.app. ")

    def transfer_to_applications(confirmation=True):
        clear()
        print(f"{brown}[Option 6 - Transfer RoSniper to /Applications]{end}")
        if os.path.exists("/Applications/RoSniper.app"):
            os.system("rm -rf /Applications/RoSniper.app")
        os.system("mv RoSniper.app /Applications/")
        if confirmation == True:
            input("RoSniper.app was moved to the Applications folder. ")

    def delete_from_applications():
        clear()
        print(f"{brown}[Option 7 - Delete RoSniper from /Applications]{end}")
        os.system("rm -rf /Applications/RoSniper.app")
        input("RoSniper.app was deleted from the Applications folder. ")

    while True:
        clear()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        print(f"{brown}[RoSniper Build Tool]{end}")
        print(f"  {bold}[1] Install RoSniper from source (Options 2, 3, 4, 5, and 6 combined){end}")
        print("  [2] Build RoSniper")

        AppExists = os.path.exists("RoSniper.app")
        AppExists_A = os.path.exists("/Applications/RoSniper.app")
        print(f"  {faint if not AppExists else ""}[3] Inject an existing changelog.txt into RoSniper.app{end if not AppExists else ""}")
        print(f"  {faint if not AppExists else ""}[4] Inject an existing commands.txt into RoSniper.app{end if not AppExists else ""}")
        print(f"  {faint if not AppExists else ""}[5] Inject an existing config.json into RoSniper.app{end if not AppExists else ""}")
        print(f"  {faint if not AppExists else ""}[6] Transfer RoSniper to /Applications{end if not AppExists else ""}")
        print(f"  {faint if not AppExists_A else ""}[7] Delete RoSniper from /Applications{end if not AppExists_A else ""}")

        print("  [8] Exit")

        option = input("\nSelect an option: ").strip()
        if not option.isnumeric() or not option in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            input("Invalid option. ")
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
                if os.path.exists("RoSniper.app"):
                    transfer_changelog()
            case 4:
                if os.path.exists("RoSniper.app"):
                    transfer_cmd_docs()
            case 5:
                if os.path.exists("RoSniper.app"):
                    transfer_config()
            case 6:
                if os.path.exists("RoSniper.app"):
                    transfer_to_applications()
            case 7:
                if os.path.exists("/Applications/RoSniper.app"):
                    delete_from_applications()
            case 8:
                exit()
elif platform.system() == "Windows":
    input("The build script is not available for Windows at this time. ")
elif platform.system() == "Linux":
    input("The build script is not available for Linux at this time. ")
