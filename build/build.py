import os
import shutil
import platform

brown = "\033[0;33m"
bold = "\033[1m"
faint = "\033[2m"
end = "\033[0m"

def clear():
    os.system("clear || cls")

op = platform.system()
if op in ["Darwin", "Windows"]:
    def build():
        clear()
        print(f"{brown}[Build RoSniper]{end}")
        print(f"{bold}Here are the minimum requirements to build RoSniper:{end}")
        print("    - 200MB+ space (app ~100MB, launcher ~2MB, rest is temporary files)")
        print("    - The modules pyinstaller==6.14.1, pyperclip==1.9.0, and requests==2.32.4")
        print("    - RoSniper.py in the (parent) directory of the build script")
        print("    - AppIcon.icns/.ico, launcher.py, and Info.plist in ./Resources/")
        print("    - Any version of RoSniper (MacOS) or RoSniper 2025.7+ (Windows)")
        print(f"\n{bold}If you're running Option 1 for a complete install:{end}")
        print("    - commands.txt and changelog.txt in the (parent) directory of the build script")
        print("    - OPTIONAL: config.json in the (parent) directory of the build script")

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

        if op == "Darwin":
            if not os.path.exists("./Resources/launcher") and os.path.exists("./Resources/launcher.py"):
                os.system("pyinstaller ./Resources/launcher.py")
                os.system("cp ./dist/launcher/launcher ./Resources/")
                os.system("rm -rf build dist *.spec")

            os.system("pyinstaller --windowed ./Resources/RoSniper.py --icon ./Resources/AppIcon.icns")
            os.system("cp -r dist/RoSniper.app .")
            os.system("cp ./Resources/launcher RoSniper.app/Contents/MacOS/")
            open("./RoSniper.app/Contents/Info.plist", "w").write(modifiedPLIST)
            os.system("rm -rf build dist *.spec ./Resources/RoSniper.py")
        else:
            os.system("pyinstaller ./Resources/RoSniper.py --icon ./Resources/AppIcon.ico")
            os.system("xcopy .\\dist\\RoSniper . /E /Q")
            shutil.rmtree("./build/")
            shutil.rmtree("./dist/")
            os.system("erase *.spec .\\Resources\\RoSniper.py /Q")

    def transfer_file(file, output=True):
        clear()
        if output:
            print(f"{brown}[Inject {file.split(".")[0]} into RoSniper]{end}")
        
        if os.path.exists(f"../{file}"):
            path = f"../{file}"
        elif os.path.exists(f"./{file}"):
            path = f"./{file}"
        elif os.path.exists(f"./Resources/{file}"):
            path = f"./Resources/{file}"
        else:
            input(f"{file} wasn't found. ")
            return

        if output:
            print(f"{file} was found in {path}.")

        executable = "copy" if op == "Windows" else "cp"
        dest = ".\\_internal\\ /Y" if op == "Windows" else "RoSniper.app/Contents/Frameworks/"
        path = path if op == "Darwin" else path.replace("/", "\\")
        os.system(f"{executable} {path} {dest}")

        if output:
            input(f"{file} was injected into RoSniper. ")

    def transfer_to_applications(output=True):
        clear()
        if output:
            print(f"{brown}[Transfer RoSniper to /Applications]{end}")

        if os.path.exists("/Applications/RoSniper.app"):
            os.system("rm -rf /Applications/RoSniper.app")
        os.system("mv RoSniper.app /Applications/")
        if output:
            input("RoSniper.app was moved to the Applications folder. ")

    def delete_from_applications():
        clear()
        print(f"{brown}[Delete RoSniper from /Applications]{end}")
        os.system("rm -rf /Applications/RoSniper.app")
        input("RoSniper.app was deleted from the Applications folder. ")

    while True:
        clear()
        os.chdir(os.path.dirname(__file__))

        app_location = "_internal" if op == "Windows" else "RoSniper.app"
        AppExists = "" if os.path.exists(app_location) else faint
        AppExists_A = "" if os.path.exists("/Applications/RoSniper.app") else faint

        print(f"{brown}[RoSniper Build Tool]{end}")
        print(f"{bold}[1] Install RoSniper from source (Options 2, 3, 4, 5{", and 6" if op == "Darwin" else ""} combined){end}")
        print("[2] Build RoSniper")
        print(f"{AppExists}[3] Inject an existing changelog.txt into RoSniper{end}")
        print(f"{AppExists}[4] Inject an existing commands.txt into RoSniper{end}")
        print(f"{AppExists}[5] Inject an existing config.json into RoSniper{end}")
        if op == "Darwin":
            print(f"{AppExists}[6] Transfer RoSniper to /Applications (macOS Only){end}")
            print(f"{AppExists_A}[7] Delete RoSniper from /Applications (macOS Only){end}")
        print(f"[{"6" if op == "Windows" else "8"}] Exit")

        option = input("\nSelect an option: ").strip()
        if not option.isnumeric() or not option in ["1", "2", "3", "4", "5", "6", "7" if op == "Darwin" else "1", "8" if op == "Darwin" else "1"]:
            input("Invalid option. ")
            continue
        else:
            option = int(option)

        match option:
            case 1:
                build()
                transfer_file("changelog.txt", output=False)
                transfer_file("commands.txt", output=False)
                transfer_file("config.json", output=False)
                if op == "Darwin":
                    transfer_to_applications(output=False)
            case 2:
                build()
            case 3:
                if os.path.exists(app_location):
                    transfer_file("changelog.txt")
            case 4:
                if os.path.exists(app_location):
                    transfer_file("commands.txt")
            case 5:
                if os.path.exists(app_location):
                    transfer_file("config.json")
            case 6:
                if os.path.exists(app_location) and op == "Darwin":
                    transfer_to_applications()
                elif op == "Windows":
                    exit()
            case 7:
                if os.path.exists("/Applications/RoSniper.app") and op == "Darwin":
                    delete_from_applications()
            case 8:
                exit()
else:
    clear()
    input("The build script is not available for Linux at this time. ")
