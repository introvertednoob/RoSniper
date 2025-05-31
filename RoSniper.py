import os
import sys
import objc
import time
import json
import requests
import pyperclip
import webbrowser
from sys import exit

version = "2025.6_rc"
os.chdir(os.path.dirname(__file__))

# Save ANSI codes to variables
gold = "\033[0;33m"
bold = "\033[1m"
underline = "\033[4m"
end = "\033[0m"

default_config = {
    "recent_users_length": 5,
    "delay": 0.01,
    "recent_users": [],
    "cookies": []
}

# Key functions for RoSniper
def clear():
    os.system("clear")

def save():
    open("config.json", "w", encoding="utf-8").write(json.dumps(config, indent=4))

def wait(secs, text=None):
    try:
        if text != None:
            print(text)
        time.sleep(secs)
    except KeyboardInterrupt:
        save()
        exit()

def delete_recent_user(user):
    if user.lower() in config["recent_users"]:
        config["recent_users"].remove(user.lower())
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
        print(f"{gold}[Add Account]{end}")
        print("Copy a .ROBLOSECURITY cookie to your clipboard.")
        print("This can be found in the Storage/Application section of your browser's console.")

        if type(pyperclip.paste()) == type(None):
            pyperclip.copy("")
        
        if not "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" in pyperclip.paste():
            pyperclip.copy("")
            while pyperclip.paste() == "":
                wait(0.1)
        cookie = pyperclip.paste()
        header = {
            "Cookie": f".ROBLOSECURITY={cookie}"
        }
        try:
            req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
            user_context = json.loads(req.text)
            config["cookies"].append(cookie)
            save()
            input(f"Cookie saved successfully. Welcome, {user_context["name"]}! ")
        except requests.exceptions.ReadTimeout:
            save()
            exit()
        except requests.exceptions.SSLError:
            input("\nCouldn't connect to the Roblox servers. Your internet may be blocking Roblox. ")
            exit()
        except requests.exceptions.ConnectTimeout:
            input("\nYour request with the Roblox servers timed out. ")
            exit()
        except json.JSONDecodeError:
            print("\nRoSniper received an unexpected response:")
            input(req.text)
        except Exception as e:
            input(f"Failed to save cookie. Error: {e}")
            exit()

        if force:
            os.execl(sys.executable, sys.executable, *sys.argv)

def run_command(command):
    global user
    global users
    global decline_first_server

    command = command.lower()
    if command in ["/cmds", "/help", "/changelog"]:
        clear()
        load_file = "commands.txt" if command in ["/cmds", "/help"] else "changelog.txt"
        title = "Commands" if command in ["/cmds", "/help"] else "Changelog"
        print(f"{gold}[{title}]{end}")
        if os.path.exists(load_file):
            text = open(load_file).read()
            text = text.replace("[green]", "\033[0;32m").replace("[bold]", bold).replace("[underline]", underline).replace("[end]", end).replace("[cur_recent_users]", str(config["recent_users_length"])).replace("[cur_delay]", str(config["delay"])).replace("[cur_df]", str(decline_first_server))
            print(text)
        else:
            print(f"{load_file} isn't present.")
        input("Press ENTER to return to the main menu. ")
    elif command.startswith("/setrecents ") or command.startswith("/set "):
        if command.split(" ")[1].isnumeric():
            config["recent_users_length"] = int(command.split(" ")[1])
            wait(1, f"\n{underline}Set the length of Recent Users to {"99 (max)" if config["recent_users_length"] > 99 else config["recent_users_length"]}.{end}")
        else:
            wait(1, f"\n{underline}Invalid length.{end}")
        save()
    elif command.startswith("/del "):
        if config["recent_users"] == []:
            wait(0.75, f"\n{underline}There are no Recent Users to delete.{end}")
        elif command.split(" ")[1] == "all":
            config["recent_users"] = []
            wait(1, f"\n{underline}Deleted all Recent Users.{end}")
        elif command.split(" ")[1].isnumeric():
            if int(command.split(" ")[1]) <= len(config["recent_users"]):
                del config["recent_users"][int(command.split(" ")[1]) - 1]
                wait(1, f"\n{underline}Deleted Recent User #{command.split(" ")[1]}.{end}")
            else:
                wait(0.75, f"\n{underline}This Recent User doesn't exist.{end}")
        elif command.split(" ")[1] in config["recent_users"]:
            config["recent_users"].remove(command.split(" ")[1])
            wait(1, f"\n{underline}Deleted Recent User [@{command.split(" ")[1]}].{end}")
        else:
            wait(0.75, f"\n{underline}This Recent User doesn't exist.{end}")
        save()
    elif command == "/logout":
        if command.endswith(" all"):
            config["cookies"] = []
            print(f"\n{underline}Removed all cookies from config.json.{end}")
        else:
            del config["cookies"][id]
            print(f"\n{underline}Deleted this account's cookie from config.json.{end}")
        save()
        wait(2, f"{bold}RoSniper will restart now.{end}")
        os.execl(sys.executable, sys.executable, *sys.argv)
    elif command in ["/addaccount", "/add"]:
        wait(1, f"\n{underline}You will be redirected to the Save Cookie menu.{end}")
        add_account(force=True)
    elif command.startswith("/delay "):
        config["delay"] = float(command.split(" ")[1]) if command.split(" ")[1].replace(".", "").isnumeric() else 0.01
        save()
        wait(0.5, f"\n{underline}Delay set to {config["delay"]}s.{end}")
    elif command in ["/df", "/declinefirst"]:
        if decline_first_server:
            decline_first_server = False
        else:
            decline_first_server = True
    else:
        similar_command = ""
        list_of_commands = ["/cmds", "/help", "/changelog", "/set", "/setrecents", "/del", "/logout", "/addaccount", "/add", "/df", "/declinefirst"]
        for cmd in list_of_commands:
            if command in cmd or cmd in command:
                similar_command = cmd
                break
        if similar_command == "":
            print(f"\n{underline}Invalid command: \"{command}\"{end}\nType /cmds to see documentation on commands.")
        elif similar_command != command:
            print(f"\n{underline}Invalid command: \"{command}\". Perhaps you meant \"{similar_command}\"?{end}\nType /cmds to see documentation on commands.")
        else:
            print(f"\n{underline}This command exists, but it requires arguments.{end}\nType /cmds to see documentation on the arguments for commands.")
        wait(2)

def client():
    global users
    global online_data
    global current_user
    global declined_servers
    global prepare_roblox
    global current_server
    global checks_since_start
    global decline_first_server

    clear()
    print(f"{gold}[Times Checked: {checks_since_start}]{end}")
    for _ in range(len(users)):
        status = online_data["userPresences"][_]["userPresenceType"]
        place_id = online_data["userPresences"][_]["placeId"]
        server_id = online_data["userPresences"][_]["gameId"]
        user_label = f"{bold + "[Priority] " + end if _ == current_user else ""}{users[_]}"

        if status == 1:
            if _ == current_user and prepare_roblox:
                webbrowser.open("roblox://")
                prepare_roblox = False
            print(f"{user_label} is on the Roblox website!")
        elif status == 2 and place_id == server_id == None:
            print(f"{user_label} has their joins off, or you aren't following them.")
            print(f"   -> Follow them @ https://roblox.com/users/{data["userIDs"][_]}/profile")
            print("   -> This screen will automatically update when you follow them.")
        elif status == 2 and current_server != server_id:
            if decline_first_server and _ == current_user:
                declined_servers += [server_id]
                decline_first_server = False

            if server_id in declined_servers:
                print(f"{user_label} is in a server you declined (roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}).")
                continue
            elif current_user != _:
                if input(f"\n{users[_]} is in a game, but you are focusing on {users[current_user]}.\nPress ENTER to focus on {users[_]}, or type 'q' to decline. ").lower().strip().startswith("q"):
                    print(f"Declined to join {users[_]}. RoSniper will still check for {users[_]}, but won't show you that server.")
                    declined_servers += [server_id]
                    
                    if input(f"   -> Would you like to focus on {users[_]}, so you can join them next time (y/n)? ").lower().strip().startswith("y"):
                        current_user = _
            
            if not server_id in declined_servers:
                webbrowser.open(f'roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}')
                print(f"{user_label} is in a game: {underline}roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}{end}")
                current_user = _
                prepare_roblox = True
                current_server = server_id
        elif status == 3:
            if not prepare_roblox:
                prepare_roblox = True
            print(f"{user_label} is in Roblox Studio.")
        elif status == 0:
            if not prepare_roblox and current_user == _:
                prepare_roblox = True
            print(f"{user_label} is offline.")
        elif current_server == server_id:
            print(f"{user_label} is in a game: {underline}roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}{end}")

def client_exception(error):
    global checks_since_start

    clear()
    print(f"{gold}[Times Checked: {checks_since_start}]{end}")
    print(error)

# Save/load config file and verify it
if os.path.exists("config.json"):
    try:
        config = json.loads(open("config.json").read())
    except Exception as e:
        os.remove("config.json")
        input(f"An error occured while loading config.json: {e} ")
        exit()
else:
    config = {}

for key in default_config.keys():
    try:
        if not key in config.keys():
            raise ValueError
        elif type(config[key]) != type(default_config[key]):
            raise ValueError
        if type(config[key]) == list:
            for item in range(len(config[key])):
                if type(config[key][item]) not in [str, objc.pyobjc_unicode]:
                    del config[key][item]
    except ValueError:
        config[key] = default_config[key]
fix_recents()
save()

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
        usernames += [json.loads(req.text)["name"]]
        display_names += [json.loads(req.text)["displayName"]]
    elif req.status_code == 429:
        clear()
        print(f"{gold}[Network Error / Too Many Requests]{end}")
        print(f"Couldn't contact the Roblox servers to authenticate you.")
        wait(5, "RoSniper will keep trying to log you in every 5s.")
        os.execl(sys.executable, sys.executable, *sys.argv)
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
            print(f"{gold}[Select an Account]{end}")
            for i in range(len(usernames)):
                print(f"  - [ID: {i + 1}] {usernames[i]}")
            print("")
            id = int(input("Enter the account you want to use: ")) - 1
        except KeyboardInterrupt:
            exit()
        except:
            id = float('inf')
            wait(0.5, "Invalid ID.")
else:
    id = 0

if len(config["cookies"]) > 0:
    header = {
        "Cookie": f".ROBLOSECURITY={config['cookies'][id]}"
    }
else:
    os.execl(sys.executable, sys.executable, *sys.argv)

user_context = {
    "name": usernames[id],
    "displayName": display_names[id]
}

decline_first_server = False
while True:
    # Show main menu
    clear()
    print(f"{gold}[RoSniper] [ver. {version}]{end}")
    print("Join-snipes accounts (that the logged-in user can join) when they join a game.")
    print(f"Be ready to join someone's server, hopefully not too deep in the queue :>")

    print(f"{gold}\n[Tips]{end}")
    print("  - Type /cmds or /help to see the full list of commands.")
    print("  - Type /changelog to see the changelog.")

    print(f"\n{gold}[Recent Users]{end}")
    for i in range(len(config["recent_users"])):
        print(f"[{i + 1}] {bold}{config["recent_users"][i]}{end}")
    if len(config["recent_users"]) == 0:
        print("No saved users! Join-snipe some users to save them to this list!")
        if config["recent_users_length"] == 5:
            print(f"You can save up to 5 users in this list by default. Run /set [MAX_LENGTH] to change this.")
        else:
            print(f"You can save up to {config["recent_users_length"]} users in this list.")
    print("")
    if decline_first_server:
        print(f"{underline}Decline First Server is Active{end}")
    print(f"Logged in as {bold}{user_context["displayName"]} (@{user_context["name"]}){end}")

    try:
        user = input("Enter username, recent user ID, or command: ").strip()
        if user == "":
            wait(0.75, f"{underline}\nA user or command is required.{end}")
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
        if len(users[user]) < 3 and users[user].isnumeric():
            if int(users[user]) <= len(config["recent_users"]):
                users[user] = config["recent_users"][int(users[user]) - 1]
            else:
                del users
                wait(0.75, f"{underline}\nRecent user not avaliable.{end}")
                break

        # You can't RoSnipe yourself!
        if users[user].lower() == user_context["name"].lower():
            wait(0.5, f"{underline}\nYou can't RoSnipe yourself.{end}")
            delete_recent_user(users[user])
            del users
            break

    if not "users" in globals():
        continue

    # Validate the username(s) provided
    current_iterated_user = ""
    try:
        data = {
            "userIDs": []
        }
        for user in users:
            current_iterated_user = user
            usernames = {
                "usernames": [user]
            }
            req = requests.post("https://users.roblox.com/v1/usernames/users", json=usernames)
            if not int(json.loads(req.text)["data"][0]["id"]) in data["userIDs"]:
                data["userIDs"] += [int(json.loads(req.text)["data"][0]["id"])]
            else:
                raise ValueError
    except ValueError:
        wait(1, f"{underline}\nYou can't snipe the same user twice.{end}")
        continue
    except requests.exceptions.SSLError:
        wait(1.5, f"{underline}Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.{end}")
        continue
    except Exception as e:
        delete_recent_user(current_iterated_user)
        wait(1.5, f"{underline}\nWe searched far and wide, but the user [@{current_iterated_user}] doesn't exist.{end}")
        continue

    # Save usernames to recent users
    for user in users:
        delete_recent_user(user)
        config["recent_users"].insert(0, user.lower())
    fix_recents()

    # Start RoSniper
    clear()
    current_user = 0
    current_server = ""
    declined_servers = []
    prepare_roblox = True
    checks_since_start = 0

    session = requests.Session()
    session.headers.update(header)

    while True:
        try:
            checks_since_start += 1
            req = session.post(url="https://presence.roblox.com/v1/presence/users", json=data, timeout=5)
            if req.ok:
                online_data = json.loads(req.content.decode())
                client()
                time.sleep(config["delay"])
            else:
                client_exception(f"<{req.status_code}> Couldn't connect to the Roblox servers.")
        except requests.exceptions.ConnectionError:
            client_exception("[ConnectionError] Couldn't connect to the Roblox servers. Retrying in 1s...")
            wait(1)
        except requests.exceptions.SSLError:
            client_exception("[SSLError] Couldn't connect to the Roblox servers. Your internet may be blocking Roblox. ")
            break
        except requests.exceptions.ConnectTimeout:
            client_exception("[ConnectTimeout] Your request with the Roblox servers timed out. ")
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            client_exception(f"An error occured: {e} ")
    session.close()
    decline_first_server = False