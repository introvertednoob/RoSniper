import os
import shutil
import platform

brown = "\033[0;33m"
bold = "\033[1m"
faint = "\033[2m"
end = "\033[0m"

def clear():
    os.system("clear || cls")

if platform.system() == "Windows":
    def build():
        clear()
        print(f"{brown}[Build RoSniper for Windows (beta)]{end}")
        print(f"{bold}Here are the minimum requirements to build RoSniper for Windows:{end}")
        print("    - 200MB+ space (app ~100MB, launcher ~2MB, rest is temporary files)")
        print("    - The modules pyinstaller==6.14.1, pyperclip==1.9.0, and requests==2.32.4")
        print("    - RoSniper.py in the (parent) directory of the build script")
        print("    - AppIcon.icns, launcher.py, and Info.plist in ./Resources/")
        print("    - RoSniper 2025.7+")
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
        modifiedRoSniper = open(RoSniperPath, "r").read().replace(f"version = \"{listedVersion}\"", f"version = \"{version}\"")
        open("./Resources/RoSniper.py", "w").write(modifiedRoSniper)
        
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
            if output:
                print(f"{file} was found in the parent directory.")
            os.system(f"copy ..\\{file} .\\_internal\\ /Y")
        elif os.path.exists(f"./{file}"):
            if output:
                print(f"{file} was found in this directory.")
            os.system(f"copy ..\\{file} .\\_internal\\ /Y")
        elif os.path.exists(f"./Resources/{file}"):
            if output:
                print(f"{file} was found in the Resources directory.")
            os.system(f"copy ..\\{file} .\\_internal\\ /Y")
        else:
            input(f"{file} wasn't found. ")
            return

        if output:
            input(f"{file} was injected into RoSniper. ")

    while True:
        clear()
        os.chdir(os.path.dirname(__file__))

        AppExists = "" if os.path.exists("./_internal/") else faint

        print(f"{brown}[RoSniper Build Tool]{end}")
        print(f"{bold}[1] Install RoSniper from source (Options 2, 3, 4, 5, and 6 combined){end}")
        print("[2] Build RoSniper")
        print(f"{AppExists}[3] Inject an existing changelog.txt into RoSniper.app{end}")
        print(f"{AppExists}[4] Inject an existing commands.txt into RoSniper.app{end}")
        print(f"{AppExists}[5] Inject an existing config.json into RoSniper.app{end}")
        print("[6] Exit")

        option = input("\nSelect an option: ").strip()
        if not option.isnumeric() or not option in ["1", "2", "3", "4", "5", "6"]:
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
            case 2:
                build()
            case 3:
                if os.path.exists("./_internal/"):
                    transfer_file("changelog.txt")
            case 4:
                if os.path.exists("./_internal/"):
                    transfer_file("commands.txt")
            case 5:
                if os.path.exists("./_internal/"):
                    transfer_file("config.json")
            case 6:
                exit()
elif platform.system() == "Darwin":
    input("Please use the macOS build script. ")
elif platform.system() == "Linux":
    input("Linux is not supported. ")
