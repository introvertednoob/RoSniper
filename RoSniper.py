import os
import objc
import time
import json
import webbrowser
import requests
import pyperclip

version = "2025.1"
os.chdir(os.path.dirname(__file__))

# Save ANSI codes to variables
BROWN = "\033[0;33m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"

# Key functions for RoSniper
def clear():
    os.system("clear")

def save():
    open("config.json", "w", encoding="utf-8").write(json.dumps(config, indent=4))

def check_config():
    defaultConfig = {
        "recent_users_length": 5,
        "delay": 0.01,
        "recent_users": [],
        "cookies": []
    }

    for key in defaultConfig.keys():
        try:
            if not key in config.keys():
                raise ValueError
            elif type(config[key]) != type(defaultConfig[key]):
                raise ValueError
            if type(config[key]) == list:
                for item in range(len(config[key])):
                    if type(config[key][item]) not in [str, objc.pyobjc_unicode]:
                        del config[key][item]
        except ValueError:
            config[key] = defaultConfig[key]

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
        print(f"{BROWN}[Add Account]{END}")
        print("Copy a .ROBLOSECURITY cookie to your clipboard.")
        print("This can be found in the Storage/Application section of your browser's console.")
        try:
            if type(pyperclip.paste()) == type(None):
                pyperclip.copy("")
            
            if not "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" in pyperclip.paste():
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

            if force:
                os.execl(os.sys.executable, os.sys.executable, *os.sys.argv)
        except Exception as e:
            input(f"Failed to save cookie. Error: {e}")
            exit()

def run_command(command):
    global users
    global user

    command = command.lower()
    if command == "/cmds":
        clear()
        print(f"{BROWN}[Commands]{END}")
        print(f"{UNDERLINE}/cmds{END}\n  -> Shows this window\n")
        print(f"{UNDERLINE}/changelog{END}\n  -> Shows the RoSniper changelog\n")
        print(f"{UNDERLINE}/setRecents [MAX_LENGTH]{END} or {UNDERLINE}/set [MAX_LENGTH]{END}\n  -> Sets the max length of Recent Users\n    - Default: 5 users\n    - Currently: {config['recent_users_length']} users\n    - Maximum: 99 users\n")
        print(f"{UNDERLINE}/logout (all){END}\n  -> Removes current account or all accounts from config.json\n")
        print(f"{UNDERLINE}/add{END} or {UNDERLINE}/addAccount{END}\n  -> Adds a new account\n")
        print(f"{UNDERLINE}/delay [SECONDS]{END}\n  -> Sets the delay between requests\n    - Default: 0.01s\n    - Currently: {config['delay']}s\n")
        print(f"{UNDERLINE}/del [RECENT_USER] | [RECENT_USER_INDEX] | all{END}\n  -> Deletes a specific user or all users from the Recent Users list\n")
        print(f"{UNDERLINE}/exit{END}\n  -> Exits RoSniper\n")
        print(f"Words in brackets represent values (ex: {BOLD}[SECONDS]{END} means {BOLD}the # of seconds{END}).")
        input("Press ENTER to return to the main menu. ")
    elif command == "/changelog":
        clear()
        print(f"{BROWN}[Changelog]{END}")
        if os.path.exists("changelog.txt"):
            changelog = open("changelog.txt").read()
            changelog = changelog.replace("[BOLD]", BOLD).replace("[UNDERLINE]", UNDERLINE).replace("[END]", END)
            print(changelog)
        else:
            print("changelog.txt isn't present.")
        print(f"\nDevelopment on RoSniper started in May 2024.")
        print(f"{BOLD}There are a lot of undocumented changes from May to now.{END}")
        input("\nPress ENTER to return to the main menu. ")
    elif command.startswith("/setrecents ") or command.startswith("/set "):
        try:
            if command.split(" ")[1].isnumeric():
                config["recent_users_length"] = int(command.split(" ")[1])
                print(f"\n{UNDERLINE}Set the length of Recent Users to {"99 (max)" if config["recent_users_length"] > 99 else config["recent_users_length"]}.{END}")
                time.sleep(1)
            else:
                print(f"\n{UNDERLINE}Invalid length.{END}")
                time.sleep(1)
            save()
        except:
            pass
    elif command.startswith("/del "):
        if config["recent_users"] == []:
            print(f"\n{UNDERLINE}There are no Recent Users to delete.{END}")
            time.sleep(0.75)
        elif command.split(" ")[1] == "all":
            config["recent_users"] = []
            print(f"\n{UNDERLINE}Deleted all Recent Users.{END}")
            time.sleep(1)
        elif command.split(" ")[1].isnumeric():
            if int(command.split(" ")[1]) <= len(config["recent_users"]):
                del config["recent_users"][int(command.split(" ")[1]) - 1]
                print(f"\n{UNDERLINE}Deleted Recent User #{command.split(" ")[1]}.{END}")
                time.sleep(1)
            else:
                print(f"\n{UNDERLINE}This Recent User doesn't exist.{END}")
                time.sleep(0.75)
        elif command.split(" ")[1] in config["recent_users"]:
            config["recent_users"].remove(command.split(" ")[1])
            print(f"\n{UNDERLINE}Deleted Recent User [@{command.split(" ")[1]}].{END}")
            time.sleep(1)
        else:
            print(f"\n{UNDERLINE}This Recent User doesn't exist.{END}")
            time.sleep(0.75)
        save()
    elif command == "/logout":
        if command.endswith(" all"):
            config["cookies"] = []
            print(f"\n{UNDERLINE}Removed all cookies from config.json.{END}")
            print("Restart RoSniper for this to take effect.")
            time.sleep(1)
        else:
            del config["cookies"][id]
            print(f"\n{UNDERLINE}Deleted this account's cookie from config.json.{END}")
            print("Restart RoSniper for this to take effect.")
            time.sleep(1)
        save()
    elif command in ["/addaccount", "/add"]:
        print(f"\n{UNDERLINE}You will be redirected to the Save Cookie menu.{END}")
        time.sleep(1)
        add_account(force=True)
    elif command.startswith("/delay "):
        if command.split(" ")[1].replace(".", "").isnumeric():
            config["delay"] = float(command.split(" ")[1])
            save()
        print(f"\n{UNDERLINE}Delay set to {command.split(" ")[1]}s.{END}")
        time.sleep(0.5)
    elif command == "/exit":
        exit()
    else:
        similarCommand = ""
        listOfCommands = ["/cmds", "/changelog", "/set", "/setrecents", "/del", "/logout", "/addaccount", "/add", "/exit"]
        for cmd in listOfCommands:
            if command in cmd:
                similarCommand = cmd
                break
        if similarCommand == "":
            print(f"\n{UNDERLINE}Invalid command: '{command}'{END}\nType /cmds to see documentation on commands.")
        elif similarCommand != command:
            print(f"\n{UNDERLINE}Invalid command: '{command}'. Perhaps you meant '{similarCommand}'?{END}\nType /cmds to see documentation on commands.")
        else:
            print(f"\n{UNDERLINE}This command exists, but it requires arguments.{END}\nType /cmds to see documentation on the arguments for commands.")
        time.sleep(2)

def client():
    global users
    global currentUser
    global prepareRoblox
    global declinedServers
    global onlineData
    global oldServerToken
    global checksSinceStart

    clear()
    print(f"{BROWN}[Times Checked: {checksSinceStart}]{END}")
    for _ in range(len(users)):
        onlineStatus = onlineData["userPresences"][_]["userPresenceType"]

        if onlineStatus == 1:
            if _ == currentUser and prepareRoblox:
                webbrowser.open("roblox://")
                prepareRoblox = False
            print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} is on the Roblox website!")
        elif onlineStatus == 2 and oldServerToken != onlineData["userPresences"][_]["gameId"]:
            gameID = onlineData["userPresences"][_]["placeId"]
            serverID = onlineData["userPresences"][_]["gameId"]

            if serverID in declinedServers:
                print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} is in a server you declined.")
                continue
            elif currentUser != _:
                overrideCurrentUser = input(f"{"\n" if _ > 0 else ""}{users[_]} is in a game, but you are focusing on {users[currentUser]}.\nPress ENTER to focus on {users[_]}, or type 'q' to decline. ").lower().strip()
                if overrideCurrentUser.startswith("q"):
                    print(f"Declined to join {users[_]}. RoSniper will still check for {users[_]}, but won't show you that server.")
                    declinedServers += [onlineData["userPresences"][_]["gameId"]]
                    
                    if input(f"   -> Would you like to focus on {users[_]}, so you can join them next time (y/n)? ").lower().strip().startswith("y"):
                        currentUser = _
            
            if not serverID in declinedServers:
                webbrowser.open(f'roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}')
                print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} is in a game: {UNDERLINE}roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}{END}")
                currentUser = _
                prepareRoblox = True
                oldServerToken = serverID
                continue
        elif onlineStatus == 2 and onlineData["userPresences"][_]["gameId"] == None and onlineData["userPresences"][_]["placeId"] == None:
            print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} has their joins off, or you aren't following them.")
            print(f"   -> Follow them @ https://roblox.com/users/{data["userIDs"][_]}/profile")
        elif onlineStatus == 3:
            if not prepareRoblox:
                prepareRoblox = True
            print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} is in Roblox Studio.")
        elif onlineStatus == 0:
            if not prepareRoblox and currentUser == _:
                prepareRoblox = True
            print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} is offline.")
        elif oldServerToken == onlineData["userPresences"][_]["gameId"]:
            gameID = onlineData["userPresences"][_]["placeId"]
            serverID = onlineData["userPresences"][_]["gameId"]
            print(f"{BOLD+"[Priority] "+END if _ == currentUser else ""}{users[_]} is in a game: {UNDERLINE}roblox://experiences/start?placeId={gameID}&gameInstanceId={serverID}{END}")

# Save/load config file and verify it
if os.path.exists("config.json"):
    try:
        config = json.loads(open("config.json").read())
    except Exception as e:
        input(f"An error occured: {e} ")
        os.remove("config.json")
        exit()
else:
    config = {}
check_config()

# Save .ROBLOSECURITY cookie or add a new .ROBLOSECURITY cookie
add_account()

# Verify .ROBLOSECURITY cookies
usernames = []
display_names = []
for cookie in range(len(config["cookies"])):
    header = {
        "Cookie": f".ROBLOSECURITY={config["cookies"][cookie]}"
    }
    try:
        req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
        if not req.ok:
            raise requests.exceptions.ReadTimeout
    except requests.exceptions.ReadTimeout:
        del config["cookies"][cookie]
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
        display_names += [json.loads(req.text)['displayName']]
    elif req.status_code == 429:
        clear()
        print(f"{BROWN}[Network Error / Too Many Requests]{END}")
        print(f"Couldn't contact the Roblox servers to authenticate you.")
        print("RoSniper will keep trying to log you in.")
        time.sleep(5)
        os.execl(os.sys.executable, os.sys.executable, *os.sys.argv)
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
            print(f"{BROWN}[Select an Account]{END}")
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

userContext = {
    "name": usernames[id],
    "displayName": display_names[id]
}

while True:
    # Show home screen
    check_config()
    clear()
    print(f"{BROWN}[RoSniper] [ver. {version}]{END}")
    print("Snipe-joins accounts (that the logged-in user can join) when they join a game.")
    print(f"Be ready to join someone's server, hopefully not too deep in the queue :>")

    print(f"\n{BROWN}[How To Use]{END}")
    print("  - Enter the username that you want to join below.")
    print("  - If the user is on the website, the Roblox app will launch.")
    print("  - Finally, wait a bit and be early to the server!")

    print(f"{BROWN}\n[Commands]{END}")
    print("  - Type /cmds to see the full list of commands.")
    print("  - Type /changelog to see the changelog.")

    print(f"\n{BROWN}[Recent Users]{END}")
    for i in range(0, len(config["recent_users"])):
        print(f"[{i+1}] {BOLD}{config['recent_users'][i]}{END}")
    if len(config["recent_users"]) == 0:
        print("No saved users! Join-snipe some users to save them to this list!")
        if config["recent_users_length"] == 5:
            print(f"You can save up to 5 users in this list by default. Run /set [MAX_LENGTH] to change this.")
        else:
            print(f"You can save up to {config['recent_users_length']} users in this list.")
    print("")
    print(f"Logged in as {BOLD}{userContext['displayName']} (@{userContext['name']}){END}")

    try:
        user = input("Enter username, recent user ID, or command: ").strip()
        if user == "":
            print(f"{UNDERLINE}\nA user or command is required.{END}")
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
                print(f"{UNDERLINE}\nRecent user not avaliable.{END}")
                del users
                time.sleep(0.75)
                break

        # You can't RoSnipe yourself!
        if users[user].lower() == userContext["name"].lower():
            print(f"{UNDERLINE}\nYou can't RoSnipe yourself.{END}")
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
        print(f"{UNDERLINE}\nYou can't snipe the same user twice.{END}")
        time.sleep(1)
        continue
    except:
        if currentIteratedUser in config["recent_users"]:
            config["recent_users"].remove(currentIteratedUser)
        print(f"{UNDERLINE}\nWe searched far and wide, but the user [@{currentIteratedUser}] doesn't exist.{END}")
        time.sleep(1.5)
        continue

    # Save usernames to recent users
    for user in users:
        if user.lower() in config["recent_users"]:
            config["recent_users"].remove(user.lower())
        check_config()
        config["recent_users"] = [user.lower()] + config["recent_users"]
        save()

    # Start RoSniper
    clear()
    currentUser = 0
    declinedServers = []
    prepareRoblox = True
    oldServerToken = ""
    checksSinceStart = 0

    userList = ""
    for user in range(len(users)):
        userList += users[user]
        if user != len(users) - 1:
            userList += " and "

    session = requests.Session()
    session.headers.update(header)
    while True:
        try:
            checksSinceStart += 1
            req = session.post(url="https://presence.roblox.com/v1/presence/users", json=data)
            if req.ok:
                onlineData = json.loads(req.content.decode())
                client()
                time.sleep(config["delay"])
            else:
                clear()
                print(f"{BROWN}[Times Checked: {checksSinceStart}]{END}")
                print(f"<{req.status_code}> Couldn't connect to the Roblox servers.")
        except requests.exceptions.ConnectionError:
            clear()
            print(f"{BROWN}[Times Checked: {checksSinceStart}]{END}")
            print("[ConnectionError] Couldn't connect to the Roblox servers. Retrying in 1s...")
            time.sleep(1)
        except requests.exceptions.SSLError:
            clear()
            print(f"{BROWN}[Times Checked: {checksSinceStart}]{END}")
            input("[SSLError] Couldn't connect to the Roblox servers. Your internet may be blocking Roblox. ")
            break
        except requests.exceptions.ConnectTimeout:
            clear()
            print(f"{BROWN}[Times Checked: {checksSinceStart}]{END}")
            input("[ConnectTimeout] Your request with the Roblox servers timed out. ")
            break
        except KeyboardInterrupt:
            clear()
            break
        except Exception as e:
            clear()
            print(f"{BROWN}[Times Checked: {checksSinceStart}]{END}")
            input(f"An error occured: {e} ")
    session.close()
