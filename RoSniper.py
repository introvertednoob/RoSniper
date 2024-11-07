import os
import time
import json
import webbrowser
import requests
import pyperclip

version = "2024.11.1"
os.chdir(__file__.replace(os.path.basename(__file__), ""))

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
    configEntries = ["recent_users_length", "delay", "recent_users", "cookies"]
    defaultValues = [5, 0.01, [], []]
    for i in range(0, len(configEntries)):
        try:
            temp = config[configEntries[i]]
            del temp
        except:
            config[configEntries[i]] = defaultValues[i]
            save()

def fix_recents():
    try:
        config["recent_users_length"] = round(config["recent_users_length"])
        if config["recent_users_length"] > 99:
            config["recent_users_length"] = 99
        if len(config["recent_users"]) > config["recent_users_length"]:
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
            userContext = json.loads(req.text)
            config["cookies"] += [cookie]
            save()
            input(f"Cookie saved successfully. Welcome, {userContext['name']}! ")
        except Exception as e:
            input(f"Failed to save cookie. Error: {e}")
            exit()

def run_command(command):
    global config
    global users
    global user

    if command == "/cmds":
        clear()
        print(f"{ansi.BROWN}[Commands]{ansi.END}")
        print(f"{ansi.BOLD}/cmds{ansi.END}\n  -> shows this window\n")
        print(f"{ansi.BOLD}/changelog{ansi.END}\n  -> shows the changelog\n")
        print(f"{ansi.BOLD}/setRecents [MAX_LENGTH]{ansi.END}\n  -> sets the max length of Recent Users (default: 5, currently: {config['recent_users_length']}, max: 99)\n")
        print(f"{ansi.BOLD}/clearRecents{ansi.END} or {ansi.BOLD}/clearRecentUsers{ansi.END}\n  -> clears Recent Users list\n")
        print(f"{ansi.BOLD}/logout{ansi.END} or {ansi.BOLD}/logout all{ansi.END}\n  -> removes current account or all accounts from config.py\n")
        print(f"{ansi.BOLD}/add{ansi.END} or {ansi.BOLD}/addAccount{ansi.END}\n  -> adds a new account\n")
        print(f"{ansi.BOLD}/delay [SECONDS]{ansi.END}\n  -> sets the delay between requests (default: 0.01, currently: {config['delay']})\n")
        print(f"{ansi.BOLD}/del [RECENT_USER] or [RECENT_USER_INDEX]{ansi.END}\n  -> deletes a specific user from the Recent Users list\n")
        input("Press ENTER to return to the main menu. ")
    elif command == "/changelog":
        clear()
        print(f"{ansi.BROWN}[Changelog]{ansi.END}")
        print(f"{ansi.BOLD}Version 2024.11.1:{ansi.END}")
        print("    - RoSniper now tells you if the user has their joins off/you aren't following them.")
        print("    - Fixed a bug where commands with spaces in between them wouldn't execute properly.")
        print("")
        print(f"{ansi.BOLD}Version 2024.11:{ansi.END}")
        print("    - Added a new command: /changelog")
        print("    - Added the ability to snipe multiple users at once")
        print("      - Type a comma in between usernames to snipe multiple users.")
        print("      - Recent User IDs are compatible with this as well.")
        print("    - If you already have a .ROBLOSECURITY cookie copied, RoSniper will save it automatically")
        print("    - RoSniper now restarts instantly when CTRL+C is pressed")
        print("      - Your cookies aren't checked again to save time")
        print("    - If the user is in Roblox Studio, display the correct status")
        print("    - Improved error handling for network requests")
        print("    - Set the default delay from 0.0075s -> 0.01s")
        print("    - Other minor improvements")
        print(f"\n{ansi.BOLD}Everything else was added previously.{ansi.END}")
        input("Press ENTER to return to the main menu. ")
    elif "/setrecents " in command:
        try:
            if command.split(" ")[1].isnumeric():
                config["recent_users_length"] = int(command.split(" ")[1])
            else:
                config["recent_users_length"] = 5
            save()
        except:
            pass
    elif "/del " in command:
        if command.split(" ")[1].isnumeric():
            if int(command.split(" ")[1]) <= len(config["recent_users"]):
                del config["recent_users"][int(command.split(" ")[1]) - 1]
        if command.split(" ")[1] in config["recent_users"]:
            config["recent_users"].remove(command.split(" ")[1])
        save()
    elif command in ["/clearrecentusers", "/clearrecents"]:
        config["recent_users"] = []
        save()
    elif command == "/logout":
        if command.endswith(" all"):
            config["cookies"] = []
        else:
            del config["cookies"][id]
        save()
    elif command in ["/addaccount", "/add"]:
        add_account(force=True)
    elif "/delay " in command:
        if command.split(" ")[1].replace(".", "").isnumeric():
            config["delay"] = float(command.split(" ")[1])
            save()
    else:
        input("\nInvalid command. ")

def client():
    global users
    global currentUser
    global prepareRoblox
    global declinedServers
    global onlineData
    global oldServerToken

    isOnline = onlineData["userPresences"][_]["userPresenceType"]
    if isOnline == 2 and onlineData["userPresences"][_]["gameId"] == None and onlineData["userPresences"][_]["placeId"] == None:
        print(f"{users[_]} has their joins off, or you aren't following them.")
    elif isOnline == 2 and oldServerToken != onlineData["userPresences"][_]["gameId"]:
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
                oldServerToken = serverID
                currentUser = users[_]
                webbrowser.open(f'roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}')
                clear()
                print(f"{users[_]} is PLAYING A GAME! Launching with URL {ansi.UNDERLINE}roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}{ansi.END}...", flush=True)
                currentUser = users[_]
                prepareRoblox = True
                time.sleep(0.5)
        else:
            oldServerToken = serverID
            webbrowser.open(f'roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}')
            clear()
            print(f"{users[_]} is PLAYING A GAME! Launching with URL {ansi.UNDERLINE}roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}{ansi.END}...", flush=True)
            currentUser = users[_]
            prepareRoblox = True
            time.sleep(0.5)
    elif isOnline == 0:
        print(f"{users[_]} is offline.", flush=True)
    elif isOnline == 1:
        if currentUser == 0 or users[_] == currentUser:
            if prepareRoblox:
                webbrowser.open("roblox://")
                prepareRoblox = False
        print(f"{users[_]} is on the Roblox website!", flush=True)
    elif isOnline == 3:
        print(f"{users[_]} is in Roblox Studio.", flush=True)
    elif oldServerToken == onlineData["userPresences"][_]["gameId"]:
        print(f"You are already in the same server as {users[_]}.", flush=True)
    else:
        print("Couldn't connect to the Roblox servers.", flush=True)

# Save/load config file and verify it
config = {
    "recent_users_length": 5,
    "delay": 0.01,
    "recent_users": [],
    "cookies": []
}
if not os.path.exists("config.py"):
    save()
else:
    try:
        config = eval(open("config.py").read())
    except Exception as e:
        input(f"An error occured: {e} ")
        os.remove("config.py")
        exit()
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
        except:
            id = float('inf')
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
    print("  - Type /cmds to see a list of commands.")
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
        user = input("Enter username or recent user ID to join-snipe: ").strip()
    except KeyboardInterrupt:
        exit()

    # Run commands if needed
    if user.lower().startswith("/"):
        run_command(user)
        continue

    # Check if the user enters a Recent User ID
    users = user.split(",")
    for user in range(len(users)):
        if len(users[user]) <= 2 and users[user].isnumeric():
            try:
                users[user] = config["recent_users"][int(users[user]) - 1]
            except:
                clear()
                print(f"{ansi.BROWN}[Type the right number next time.]{ansi.END}")
                input("Recent user not avaliable. ")
                del users
                break

        # You can't RoSnipe yourself!
        if users[user].lower() == userContext["name"].lower():
            clear()
            print(f"{ansi.BROWN}[Seriously? What were you thinking?]{ansi.END}")
            input("You can't RoSnipe yourself. ")
            del users
            break

    # Validate the username(s) provided
    try:
        data = {
            "userIDs": []
        }
        for user in users:
            usernames = {
                "usernames": [user]
            }
            req = requests.post("https://users.roblox.com/v1/usernames/users", json=usernames)
            if not int(json.loads(req.text)["data"][0]["id"]) in data["userIDs"]:
                data["userIDs"] += [int(json.loads(req.text)["data"][0]["id"])]
            else:
                raise ValueError
    except ValueError:
        clear()
        print(f"{ansi.BROWN}[You already tried to snipe this guy!]{ansi.END}")
        input("You can't snipe the same user twice. ")
        continue
    except:
        clear()
        print(f"{ansi.BROWN}[Couldn't find this guy anywhere!]{ansi.END}")
        input("We searched far and wide, but this user doesn't exist. ")
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
    time.sleep(0.25)
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
        except requests.exceptions.ConnectionError:
            print("Couldn't connect to the Roblox servers.", flush=True)
            time.sleep(1)
        except requests.exceptions.SSLError:
            print("Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.", flush=True)
            time.sleep(1)
            break
        except KeyboardInterrupt:
            clear()
            break
        except Exception as e:
            input("An error occured: {e} ")
            pass
