import os
import time
import json
import webbrowser
import requests
import pyperclip

version = "2024.12_b1"
os.chdir(os.path.dirname(__file__))

# Save ANSI codes to variables
class ansi:
    BROWN = "\033[0;33m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

# Key functions for RoSniper
def clear():
    os.system("clear || cls")

def save():
    global config
    open("config.py", "w").write(json.dumps(config, indent=4))

def check_config():
    global config

    defaultConfig = {
        "recent_users_length": 5,
        "delay": 0.01,
        "recent_users": [],
        "cookies": []
    }

    for key in defaultConfig.keys():
        try:
            temp = config[key]
            if type(config[key]) != type(defaultConfig[key]):
                config[key] = defaultConfig[key]
            if type(config[key]) == list:
                for _ in range(len(config[key])):
                    if type(config[key][_]) != str:
                        del config[key][_]
                        save()
            del temp
        except:
            config[key] = defaultConfig[key]
            save()

def fix_recents():
    try:
        config["recent_users_length"] = round(config["recent_users_length"])
        if config["recent_users_length"] > 99:
            config["recent_users_length"] = 99
        while len(config["recent_users"]) > config["recent_users_length"]:
            del(config["recent_users"][config["recent_users_length"]])
    except KeyError:
        config["recent_users_length"] = 5
        config["recent_users"] = []
    save()

def add_account(force=False):
    if len(config["cookies"]) == 0 or force:
        clear()
        print(f"{ansi.BROWN}[Save Cookie]{ansi.END}")
        print("Copy a .ROBLOSECURITY cookie to your clipboard.")
        print("This can be found in the Storage/Application section of your console.")
        try:
            if not "_|WARNING:-DO-NOT-SHARE-THIS" in pyperclip.paste():
                pyperclip.copy("")
                while pyperclip.paste() == "":
                    time.sleep(0.1)
            cookie = pyperclip.paste()
            header = {
                "Cookie": f".ROBLOSECURITY={cookie}"
            }
            try:
                req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
            except requests.exceptions.ReadTimeout:
                save()
                exit()
            except requests.exceptions.SSLError:
                input("\nCouldn't connect to the Roblox servers. Your internet may be blocking Roblox. ")
                exit()
            except requests.exceptions.ConnectTimeout:
                input("\nYour request with the Roblox servers timed out. ")
                exit()
            userContext = json.loads(req.text)
            config["cookies"].append(cookie)
            save()
            input(f"Cookie saved successfully. Welcome, {userContext['name']}! ")
        except Exception as e:
            input(f"Failed to save cookie. Error: {e}")
            exit()

def run_command(command):
    global config
    global users
    global user

    command = command.lower()
    if command == "/cmds":
        clear()
        print(f"{ansi.BROWN}[Commands]{ansi.END}")
        print(f"{ansi.UNDERLINE}/cmds{ansi.END}\n  -> Shows this window\n")
        print(f"{ansi.UNDERLINE}/changelog{ansi.END}\n  -> Shows the RoSniper changelog\n")
        print(f"{ansi.UNDERLINE}/setRecents [MAX_LENGTH]{ansi.END} or {ansi.UNDERLINE}/set [MAX_LENGTH]{ansi.END}\n  -> Sets the max length of Recent Users\n    - Default: 5 users\n    - Currently: {config['recent_users_length']} users\n    - Maximum: 99 users\n")
        print(f"{ansi.UNDERLINE}/logout (all){ansi.END}\n  -> Removes current account or all accounts from config.py\n")
        print(f"{ansi.UNDERLINE}/add{ansi.END} or {ansi.UNDERLINE}/addAccount{ansi.END}\n  -> Adds a new account\n")
        print(f"{ansi.UNDERLINE}/delay [SECONDS]{ansi.END}\n  -> Sets the delay between requests\n    - Default: 0.01s\n    - Currently: {config['delay']}s\n")
        print(f"{ansi.UNDERLINE}/del [RECENT_USER] | [RECENT_USER_INDEX] | all{ansi.END}\n  -> Deletes a specific user or all users from the Recent Users list\n")
        print(f"Words in brackets represent values (ex: {ansi.BOLD}[SECONDS]{ansi.END} means {ansi.BOLD}the # of seconds{ansi.END}).")
        input("Press ENTER to return to the main menu. ")
    elif command == "/changelog":
        clear()
        print(f"{ansi.BROWN}[Changelog]{ansi.END}")
        print(f"{ansi.BOLD}Version 2024.12:{ansi.END}")
        print("This update contains much-needed revamps!")
        print("    - Removed delay before starting the sniping client")
        print("    - Removed redundant code from the client function")
        print("    - If you input a blank user anywhere, it is properly handled")
        print("    - Revamped the command system")
        print("      - The command documentation has been improved")
        print("      - Commands are not case-sensitive anymore")
        print("      - Commands show output when ran correctly")
        print("      - If you type a command without arguments, RoSniper will print that")
        print("      - If you type a wrong command, RoSniper will attempt to find a similar command")
        print("    - Revamped the check config function, check_config()")
        print("      - If a value doesn't match the correct type, it is set to default")
        print("    - Revamped the error system")
        print("      - If an error pops up, you will automatically return to the main menu")
        print("      - If an invalid user is in Recent Users, it is now removed")
        print("      - If a specific user cannot be found, RoSniper will print that user specifically")
        print(f"    - Removed the commands {ansi.UNDERLINE}/clearRecents{ansi.END} and {ansi.UNDERLINE}/clearRecentUsers{ansi.END}")
        print(f"      - Use {ansi.UNDERLINE}/del all{ansi.END} instead, it performs the same function")
        print(f"    - Added command: {ansi.UNDERLINE}/set{ansi.END}")
        print(f"      - This performs the same functions as {ansi.UNDERLINE}/setRecents{ansi.END}, but is easier to type")
        print("    - Improved error handling for network requests")
        print("    - If a user is online and goes offline, adjust variables accordingly")
        print("    - Other minor improvements")
        print("")
        print(f"{ansi.BOLD}Version 2024.11.1:{ansi.END}")
        print("Minor bugfixes for November's update...")
        print("    - RoSniper now tells you if the user has their joins off/you aren't following them")
        print("    - Fixed a bug where commands with spaces in between them wouldn't execute properly")
        print("")
        print(f"{ansi.BOLD}Version 2024.11:{ansi.END}")
        print("First true overhaul since May!")
        print("    - Added a new command: /changelog")
        print("    - Added the ability to snipe multiple users at once")
        print("      - Type a comma in between usernames to snipe multiple users")
        print("      - Recent User IDs are compatible with this as well")
        print("    - If you already have a .ROBLOSECURITY cookie copied, RoSniper will save it automatically")
        print("    - RoSniper now restarts instantly when CTRL+C is pressed")
        print("      - Your cookies aren't checked again to save time")
        print("    - If the user is in Roblox Studio, display the correct status")
        print("    - Improved error handling for network requests")
        print("    - Increased the default delay from 0.0075s -> 0.01s")
        print("    - Other minor improvements")
        print(f"\nDevelopment on RoSniper started in May 2024.")
        print(f"{ansi.BOLD}There are a lot of undocumented changes from May to now.{ansi.END}")
        input("\nPress ENTER to return to the main menu. ")
    elif command.startswith("/setrecents ") or command.startswith("/set "):
        try:
            if command.split(" ")[1].isnumeric():
                config["recent_users_length"] = int(command.split(" ")[1])
                print(f"\n{ansi.UNDERLINE}Set the length of Recent Users to {config["recent_users_length"]}.{ansi.END}")
                time.sleep(1)
            else:
                print(f"\n{ansi.UNDERLINE}Invalid length.{ansi.END}")
                time.sleep(1)
            save()
        except:
            pass
    elif command.startswith("/del "):
        if config["recent_users"] == []:
            print(f"\n{ansi.UNDERLINE}There are no Recent Users to delete.{ansi.END}")
            time.sleep(1)
        elif command.split(" ")[1] == "all":
            config["recent_users"] = []
            print(f"\n{ansi.UNDERLINE}Deleted all Recent Users.{ansi.END}")
            time.sleep(1)
        elif command.split(" ")[1].isnumeric():
            if int(command.split(" ")[1]) <= len(config["recent_users"]):
                del config["recent_users"][int(command.split(" ")[1]) - 1]
            print(f"\n{ansi.UNDERLINE}Deleted Recent User #{command.split(" ")[1]}.{ansi.END}")
            time.sleep(1)
        elif command.split(" ")[1] in config["recent_users"]:
            config["recent_users"].remove(command.split(" ")[1])
            print(f"\n{ansi.UNDERLINE}Deleted Recent User [@{command.split(" ")[1]}].{ansi.END}")
            time.sleep(1)
        save()
    elif command == "/logout":
        if command.endswith(" all"):
            config["cookies"] = []
            print(f"\n{ansi.UNDERLINE}Removed all cookies from config.py.{ansi.END}")
            print("Restart RoSniper for this to take effect.")
            time.sleep(1)
        else:
            del config["cookies"][id]
            print(f"\n{ansi.UNDERLINE}Deleted this account's cookie from config.py.{ansi.END}")
            print("Restart RoSniper for this to take effect.")
            time.sleep(1)
        save()
    elif command in ["/addaccount", "/add"]:
        print(f"\n{ansi.UNDERLINE}You will be redirected to the Save Cookie menu.{ansi.END}")
        time.sleep(1)
        add_account(force=True)
    elif command.startswith("/delay "):
        if command.split(" ")[1].replace(".", "").isnumeric():
            config["delay"] = float(command.split(" ")[1])
            save()
        print(f"\n{ansi.UNDERLINE}Delay set to {command.split(" ")[1]}s.{ansi.END}")
        time.sleep(0.5)
    else:
        similarCommand = ""
        listOfCommands = ["/cmds", "/changelog", "/set", "/setrecents", "/del", "/logout", "/addaccount", "/add"]
        for cmd in listOfCommands:
            if command in cmd:
                similarCommand = cmd
                break
        if similarCommand == "":
            print(f"\n{ansi.UNDERLINE}Invalid command: '{command}'{ansi.END}\nType /cmds to see documentation on commands.")
        elif similarCommand != command:
            print(f"\n{ansi.UNDERLINE}Invalid command: '{command}'. Perhaps you meant '{similarCommand}'?{ansi.END}\nType /cmds to see documentation on commands.")
        else:
            print(f"\n{ansi.UNDERLINE}This command exists, but it requires arguments.{ansi.END}\nType /cmds to see documentation on the arguments for commands.")
        time.sleep(2)

def client():
    global users
    global currentUser
    global prepareRoblox
    global declinedServers
    global onlineData
    global oldServerToken

    isOnline = onlineData["userPresences"][_]["userPresenceType"]
    if isOnline == 2 and oldServerToken != onlineData["userPresences"][_]["gameId"]:
        gameID = onlineData["userPresences"][_]["placeId"]
        serverID = onlineData["userPresences"][_]["gameId"]

        if serverID in declinedServers:
            return
        elif currentUser != users[_] and currentUser != 0:
            clear()
            overrideCurrentUser = input(f"{users[_]} is in a game, but you are already in {currentUser}'s game.\nPress ENTER to join {users[_]}, or type 'q' to decline. ").lower().strip()
            if overrideCurrentUser.startswith("q"):
                print(f"Declined to join {users[_]}. RoSniper will still check for {users[_]}, but won't show you that server.", flush=True)
                declinedServers += [onlineData["userPresences"][_]["gameId"]]
                time.sleep(1)
        else:
            webbrowser.open(f'roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}')
            clear()
            print(f"{users[_]} is PLAYING A GAME! Launching with URL {ansi.UNDERLINE}roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}{ansi.END}...", flush=True)
            currentUser = users[_]
            prepareRoblox = True
            oldServerToken = serverID
            return

    if isOnline == 1:
        if currentUser == 0 or users[_] == currentUser:
            if prepareRoblox:
                webbrowser.open("roblox://")
                prepareRoblox = False
        print(f"{users[_]} is on the Roblox website!", flush=True)
        return
    elif isOnline == 2 and onlineData["userPresences"][_]["gameId"] == None and onlineData["userPresences"][_]["placeId"] == None:
        print(f"{users[_]} has their joins off, or you aren't following them.")
    elif isOnline == 3:
        if not prepareRoblox:
            prepareRoblox = True
        print(f"{users[_]} is in Roblox Studio.", flush=True)
    elif isOnline == 0:
        if not prepareRoblox:
            prepareRoblox = True
        print(f"{users[_]} is offline.", flush=True)
    elif oldServerToken == onlineData["userPresences"][_]["gameId"]:
        print(f"You are already in the same server as {users[_]}.", flush=True)

# Save/load config file and verify it
if os.path.exists("config.py"):
    try:
        config = eval(open("config.py").read())
    except Exception as e:
        input(f"An error occured: {e} ")
        os.remove("config.py")
        exit()
else:
    config = {}
check_config()

# Save .ROBLOSECURITY cookie or add a new .ROBLOSECURITY cookie
add_account()

# Verify .ROBLOSECURITY cookies
usernames = []
for cookie in config["cookies"]:
    header = {
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
    try:
        req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
    except requests.exceptions.ReadTimeout:
        del cookie
        save()
        continue
    except requests.exceptions.SSLError:
        print("Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.")
        exit()
    except requests.exceptions.ConnectTimeout:
        input("\nYour request with the Roblox servers timed out. ")
        exit()

    if req.ok:
        usernames += [json.loads(req.text)['name']]
    else:
        del cookie
        save()
        continue
    del header

# Select an account if more than one cookie is present
if len(config["cookies"]) > 1:
    id = float('inf')
    while len(config["cookies"]) < id:
        try:
            clear()
            print(f"{ansi.BROWN}[Select an Account]{ansi.END}")
            for i in range(0, len(usernames)):
                print(f"  - [ID: {i+1}] {usernames[i]}")
            print("")
            id = int(input("Enter the account you want to use: ")) - 1
        except KeyboardInterrupt:
            exit()
        except:
            print("Invalid ID.")
            id = float('inf')
            time.sleep(0.5)
else:
    id = 0

header = {
    "Cookie": f".ROBLOSECURITY={config['cookies'][id]}"
}

try:
    req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
except requests.exceptions.ReadTimeout:
    del cookie
    save()
except requests.exceptions.SSLError:
    print("Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.")
    exit()
except requests.exceptions.ConnectTimeout:
    input("\nYour request with the Roblox servers timed out. ")
    exit()

if req.ok:
    userContext = json.loads(req.text)
else:
    del config["cookies"][id]
    save()
    input("The selected cookie is invalid. ")
    exit()

while True:
    # Show home screen
    check_config()
    fix_recents()
    clear()
    print(f"{ansi.BROWN}[RoSniper] [ver. {version}]{ansi.END}")
    print("Snipe-joins accounts (that the logged-in user can join) when they join a game.")
    print(f"Be ready to join someone's server, hopefully not too deep in the queue :>")

    print(f"\n{ansi.BROWN}[How To Use]{ansi.END}")
    print("  - Enter the username that you want to join below.")
    print("  - If the user is on the website, the Roblox app will launch.")
    print("  - Finally, wait a bit and be early to the server!")

    print(f"{ansi.BROWN}\n[Commands]{ansi.END}")
    print("  - Type /cmds to see the full list of commands.")
    print("  - Type /changelog to see the changelog.")

    print(f"\n{ansi.BROWN}[Recent Users]{ansi.END}")
    for i in range(0, len(config["recent_users"])):
        print(f"[{i+1}] {ansi.BOLD}{config['recent_users'][i]}{ansi.END}")
    if len(config["recent_users"]) == 0:
        print("No saved users! Join-snipe some users to save them to this list!")
        if config["recent_users_length"] == 5:
            print(f"You can save up to 5 users in this list by default.")
        else:
            print(f"You can save up to {config['recent_users_length']} users in this list.")
    print("")
    print(f"Logged in as {ansi.BOLD}{userContext['displayName']} (@{userContext['name']}){ansi.END}")

    try:
        user = input("Enter username, recent user ID, or command: ").strip()
        if user == "":
            print(f"{ansi.UNDERLINE}\nA user or command is required.{ansi.END}")
            time.sleep(0.75)
            continue
    except KeyboardInterrupt:
        exit()

    # Run commands if needed
    if user.lower().startswith("/"):
        run_command(user)
        continue

    # Check if the user enters a Recent User ID
    users = user.replace(" ", "").split(",")
    if "" in users:
        users.remove("")
    for user in range(len(users)):
        if len(users[user]) <= 2 and users[user].isnumeric():
            try:
                users[user] = config["recent_users"][int(users[user]) - 1]
            except:
                print(f"{ansi.UNDERLINE}\nRecent user not avaliable.{ansi.END}")
                del users
                time.sleep(0.75)
                break

        # You can't RoSnipe yourself!
        if users[user].lower() == userContext["name"].lower():
            print(f"{ansi.UNDERLINE}\nYou can't RoSnipe yourself.{ansi.END}")
            if users[user].lower() in config["recent_users"]:
                config["recent_users"].remove(users[user].lower())
            del users
            time.sleep(0.5)
            break

    try:
        temp = users
        del temp
    except:
        continue

    # Validate the username(s) provided
    currentIteratedUser = ""
    try:
        data = {
            "userIDs": []
        }
        for user in users:
            currentIteratedUser = user
            usernames = {
                "usernames": [user]
            }
            req = requests.post("https://users.roblox.com/v1/usernames/users", json=usernames)
            if not int(json.loads(req.text)["data"][0]["id"]) in data["userIDs"]:
                data["userIDs"] += [int(json.loads(req.text)["data"][0]["id"])]
            else:
                raise ValueError
    except ValueError:
        print(f"{ansi.UNDERLINE}\nYou can't snipe the same user twice.{ansi.END}")
        time.sleep(1)
        continue
    except:
        if currentIteratedUser in config["recent_users"]:
            config["recent_users"].remove(currentIteratedUser)
        print(f"{ansi.UNDERLINE}\nWe searched far and wide, but the user [@{currentIteratedUser}] doesn't exist.{ansi.END}")
        time.sleep(1.5)
        continue

    # Save usernames to recent users
    for user in users:
        if user.lower() in config["recent_users"]:
            config["recent_users"].remove(user.lower())
        fix_recents()
        config["recent_users"] = [user.lower()] + config["recent_users"]
        save()

    # Start RoSniper
    clear()
    currentUser = 0
    declinedServers = []
    prepareRoblox = True
    oldServerToken = ""

    userList = ""
    for user in range(len(users)):
        userList += users[user]
        if user != len(users) - 1:
            userList += " and "

    print(f"You are sniping {ansi.BROWN}{userList}{ansi.END}")
    print("Get ready to join.\n")
    session = requests.Session()
    session.headers.update(header)
    while True:
        try:
            req = session.post(url="https://presence.roblox.com/v1/presence/users", json=data)
            if req.ok:
                onlineData = json.loads(req.content.decode())
                for _ in range(len(onlineData["userPresences"])):
                    client()
                time.sleep(config["delay"])
            else:
                print("Couldn't connect to the Roblox servers.", flush=True)
        except requests.exceptions.ConnectionError:
            print("Couldn't connect to the Roblox servers.", flush=True)
            time.sleep(1)
        except requests.exceptions.SSLError:
            print("Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.", flush=True)
            time.sleep(1)
            break
        except requests.exceptions.ConnectTimeout:
            input("\nYour request with the Roblox servers timed out. ")
            break
        except KeyboardInterrupt:
            clear()
            break
        except Exception as e:
            input(f"An error occured: {e} ")
            pass
