import os
import sys
import time
import json
import getpass
import requests
import platform
import pyperclip
import webbrowser
import browser_cookie3
from sys import exit

op = platform.system()
if op == "Windows":
    import subprocess

if getattr(sys, 'frozen', False):
    if len(sys.argv) >= 2 and sys.argv[0] == sys.argv[1]:
        sys.argv.pop(1)

version = "1.5.1"
os.chdir(os.path.dirname(__file__))

# Save ANSI codes to variables
gold = "\033[0;33m"
bold = "\033[1m"
underline = "\033[4m"
end = "\033[0m"

# Define exception and default config dicts
errors = {
    "requests.exceptions.ConnectionError": "[ConnectionError] Couldn't connect to the Roblox servers.",
    "requests.exceptions.ConnectTimeout": "[ConnectTimeout] Your request with the Roblox servers timed out.",
    "requests.exceptions.SSLError": "[SSLError] Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.",
    "requests.exceptions.ReadTimeout": "[ReadTimeout] Your request with the Roblox servers timed out."
}

default_config = {
    "recent_users_length": 5,
    "delay": 0.01,
    "recent_users": [],
    "cookies": []
}

def open_link(url):
    if op == "Darwin":
        os.system(f"open \"{url}\"")
    else:
        webbrowser.open(url)

clear_cmd = "clear" if op == "Darwin" else "cls"
def clear(definite=True):
    if op == "Darwin" and definite:
        os.system("clear; clear")
    else:
        os.system(clear_cmd)

def save():
    with open("config.json", "w", encoding="utf-8") as cfg:
        json.dump(config, cfg, indent=4)

def wait(secs, text=False):
    try:
        if text:
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
    if config["recent_users_length"] > 99:
        config["recent_users_length"] = 99
    while len(config["recent_users"]) > config["recent_users_length"]:
        del config["recent_users"][config["recent_users_length"]]
    save()

def get_cookie(browser):
    try:
        cj = getattr(browser_cookie3, browser)(domain_name='roblox.com')
        for cookie in cj:
            if cookie.name == ".ROBLOSECURITY":
                return cookie.value
        return None
    except Exception as e:
        print(f"Error reading cookies: {e}")
        return None

def verify_cookie(cookie):
    global session
    global usernames
    global display_names

    header = {
        "Cookie": f".ROBLOSECURITY={config["cookies"][cookie]}"
    }
    try:
        req = session.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
        if not req.ok:
            del config["cookies"][cookie]
            save()
            return
    except Exception as e:
        if str(e) in errors.keys():
            clear()
            input(errors[str(e)])
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
        return
    del header

def add_account(restart):
    clear()
    print(f"{gold}[Add Account]{end}")
    print(f"{bold}Copy a .ROBLOSECURITY cookie to your clipboard.{end}")
    print("This can be found in the Storage/Application section of your browser's console.")
    print("Login to your Roblox account here: https://roblox.com/")    

    print(f"\n{bold}Or, copy a browser name to fetch the cookie from that browser:{end}")
    print("getsafari, getchrome, getedge, getfirefox, getall")

    if type(pyperclip.paste()) == type(None):
        pyperclip.copy("")

    while not True in [pyperclip.paste().startswith("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"), "get" in pyperclip.paste()]:
        pyperclip.copy("")
        wait(0.1)

    if "get" in pyperclip.paste() and pyperclip.paste() in ["getsafari", "getchrome", "getedge", "getfirefox", "getall"]:
        cookie = get_cookie(browser=pyperclip.paste().replace("get", "").replace("all", "load"))
    else:
        cookie = pyperclip.paste()

    if cookie in config["cookies"]:
        pyperclip.copy("")
        input("\nThis cookie already exists. ")
        return

    try:
        req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers={"Cookie": f".ROBLOSECURITY={cookie}"})
        if not req.ok:
            pyperclip.copy("")
            input("\nInvalid cookie. Restart RoSniper to try again. ")
            exit()
        config["cookies"] += [cookie]
        save()
        pyperclip.copy("")
        input(f"\nCookie saved successfully. Welcome, {json.loads(req.text)["name"]}! ")
    except Exception as e:
        if str(e) in errors.keys():
            input(f"\n{errors[str(e)]} ")
        exit()

    if restart:
        os.execl(sys.executable, sys.executable, *sys.argv)

def run_command(command):
    global monitoring
    global decline_first_server

    arg = command.split(" ")[1] if len(command.split(" ")) > 1 else ""
    if command in ["/cmds", "/changelog"]:
        clear()
        load_file = f"./assets/{"commands" if command == "/cmds" else "changelog"}.txt"
        if os.path.exists(load_file):
            print(open(load_file).read().replace("[green]", "\033[0;32m").replace("[gold]", gold).replace("[bold]", bold).replace("[underline]", underline).replace("[end]", end).replace("[cur_recent_users]", str(config["recent_users_length"])).replace("[cur_delay]", str(config["delay"])).replace("[cur_df]", str(decline_first_server)).replace("[cur_m]", str(monitoring)))
        else:
            print(f"The file ./assets/{load_file} isn't present.")
        input("Press ENTER to return to the main menu. ")
    elif command.startswith("/setrecents ") or command.startswith("/set "):
        if arg.isnumeric():
            config["recent_users_length"] = 99 if int(arg) > 99 else int(arg)
            wait(1, f"{nl}{underline}Set the length of Recent Users to {"99 (max)" if config["recent_users_length"] > 99 else config["recent_users_length"]}.{end}")
        else:
            wait(1, f"{nl}{underline}Invalid length.{end}")
        save()
    elif command.startswith("/del "):
        if config["recent_users"] == []:
            wait(0.75, f"{nl}{underline}There are no Recent Users to delete.{end}")
        elif arg == "*":
            config["recent_users"] = []
            wait(1, f"{nl}{underline}Deleted all Recent Users.{end}")
        elif arg in config["recent_users"]:
            config["recent_users"].remove(arg)
            wait(1, f"{nl}{underline}Deleted Recent User [@{arg}].{end}")
        elif arg.isnumeric():
            if int(arg) <= len(config["recent_users"]):
                recent_user_name = config["recent_users"][int(arg) - 1]
                del config["recent_users"][int(arg) - 1]
                wait(1.25, f"{nl}{underline}Deleted Recent User #{arg} (@{recent_user_name}).{end}")
            else:
                wait(0.75, f"{nl}{underline}This Recent User doesn't exist.{end}")
        else:
            wait(0.75, f"{nl}{underline}This Recent User doesn't exist.{end}")
        save()
    elif command.startswith("/logout"):
        if arg == "":
            del config["cookies"][id]
            print(f"{nl}{underline}Deleted this account's cookie from config.json.{end}")
        elif arg == "*":
            config["cookies"] = []
            print(f"{nl}{underline}Removed all cookies from config.json.{end}")
        else:
            wait(2, f"{nl}{underline}Invalid argument. See /cmds for proper documentation.{end}")
            return
        save()
        wait(1.5, f"{bold}RoSniper will restart now.{end}")
        os.execl(sys.executable, sys.executable, *sys.argv)
    elif command in ["/addaccount", "/add"]:
        wait(1, f"{nl}{underline}You will be redirected to the Save Cookie menu.{end}")
        add_account(True)
    elif command.startswith("/delay "):
        config["delay"] = float(arg) if arg.replace(".", "").isnumeric() else 0.01
        save()
        wait(0.5, f"{nl}{underline}Delay set to {config["delay"]}s.{end}")
    elif command in ["/df", "/declinefirst"]:
        decline_first_server = False if decline_first_server else True
        if decline_first_server:
            monitoring = False
    elif command in ["/m", "/monitoring"]:
        decline_first_server = False
        monitoring = False if monitoring else True
    elif command == "/alias":
        if op == "Darwin":
            clear()
            if getattr(sys, "frozen", False):
                snipe_alias = f'alias snipe="{sys.executable}"'
            else:
                snipe_alias = f'alias snipe="{sys.executable} {__file__}"'
            print(f"{gold}[Add ZSH Alias]{end}")
            print(f"The ZSH alias <snipe> will be created, which will point to RoSniper.")
            print(f"See /cmds for more information on the alias.")
            print(f"To remove the <snipe> alias, delete the entry from ~/.zshrc.")

            print(f"\n{bold}Full Alias Code: '{snipe_alias}'{end}")
            input(f"Press ENTER to confirm adding the alias <{underline}snipe{end}> to your ZSH aliases. ")
            if not os.path.exists(f"/Users/{getpass.getuser()}/.zshrc"):
                open(f"/Users/{getpass.getuser()}/.zshrc", "w").write(f"\n{snipe_alias}")
            else:
                if not "alias snipe=" in open(f"/Users/{getpass.getuser()}/.zshrc").read():
                    open(f"/Users/{getpass.getuser()}/.zshrc", "a").write(f"\n{snipe_alias}")
                else:
                    wait(1, f"\n{underline}The <snipe> alias was already added.{end}")
                    return
            wait(1, f"\n{underline}Successfully added the <snipe> alias.{end}")
        else:
            wait(1, f"{nl}{underline}You must be using macOS to run this command.{end}")
    elif command.startswith("/donate "):
        donations = json.loads(open("./assets/donations.json").read())
        if arg in donations.keys():
            print(f"{nl}{underline}Thank you for donating! Donations help keep RoSniper free for all! - @Awij126{end}")
            wait(4, f"A gamepass for {bold}{arg} Robux{end} will open shortly.")
            webbrowser.open(donations[arg])
        else:
            wait(1, f"{nl}{underline}Invalid donation amount. See /cmds for valid donation amounts.{end}")
    else:
        similar_commands = []
        list_of_commands = ["/cmds", "/changelog", "/set", "/setrecents", "/delay", "/del", "/logout", "/add", "/addaccount", "/df", "/declinefirst", "/alias", "/m", "/monitoring", "/donate"]
        for cmd in list_of_commands:
            if command in cmd or cmd in command:
                similar_commands += [cmd]
        if len(similar_commands) == 0 or similar_commands == list_of_commands:
            wait(2, f"{nl}{underline}Invalid command: \"{command}\"{end}\nType /cmds to see documentation on commands.")
        elif command in list_of_commands:
            wait(2, f"{nl}{underline}This command exists, but it requires arguments.{end}\nType /cmds to see documentation on the arguments for commands.")
        else:
            wait(2 + 0.25 * len(similar_commands), f"{nl}{underline}Invalid command: \"{command}\". Perhaps you meant \"{"\", \"".join(similar_commands)}\"?{end}\nType /cmds to see documentation on commands.")

# Client + exception code
def client():
    global users
    global online_data
    global current_user
    global declined_servers
    global prepare_roblox
    global current_server
    global checks_since_start

    global monitoring
    global decline_first_server

    clear(False)
    print(f"{gold}[Times Checked: {checks_since_start}] [Account: @{usernames[id]}]{end}")
    if monitoring:
        print(f"{bold}You're currently in Monitoring Only Mode. Join-sniping is disabled.{end}")
        print("Press CTRL+C at any time to copy information.\n")
    elif decline_first_server:
        print(f"{bold}You're currently using Decline First Server.{end}")
        print(f"The first server the priority user (@{users[current_user]}) joins will be declined.\n")

    for _ in range(len(users)):
        status = online_data["userPresences"][_]["userPresenceType"]
        place_id = online_data["userPresences"][_]["placeId"]
        server_id = online_data["userPresences"][_]["gameId"]
        user_label = f"{bold + "[Priority] " + end if _ == current_user and not monitoring else ""}{users[_]}"

        if status == 1:
            if _ == current_user and prepare_roblox and not monitoring:
                if op == "Darwin":
                    open_link("roblox://")
                else:
                    subprocess.run(["taskkill", "/f", "/im", "RobloxPlayerBeta.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                current_server = ""
                prepare_roblox = False
            print(f"{user_label} is on the Roblox website!")
        elif status == 2 and place_id == server_id == None:
            print(f"{user_label} has their joins off, or you aren't following them.")
            print(f"   -> Follow them @ https://roblox.com/users/{data["userIDs"][_]}/profile")
            print("   -> This screen will automatically update when you follow/friend the user.")
        elif status == 2 and current_server != server_id:
            if decline_first_server and _ == current_user:
                declined_servers += [server_id]
                decline_first_server = False

            if server_id in declined_servers:
                print(f"{user_label} is in a server you declined (roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}).")
                continue
            elif current_user != _ and not monitoring:
                if input(f"\n{users[_]} is in a game, but you are focusing on {users[current_user]}.\nPress ENTER to focus on {users[_]}, or type 'q' to decline. ").lower().strip().startswith("q"):
                    print(f"Declined to join {users[_]}. RoSniper will still check for {users[_]}, but won't show you that server.")
                    declined_servers += [server_id]

                    if input(f"   -> Would you like to focus on {users[_]}, so you can join them next time (y/n)? ").lower().strip().startswith("y"):
                        current_user = _

            if not server_id in declined_servers:
                if not monitoring:
                    open_link(f'roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}')
                print(f"{user_label} is in a game: {underline}roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}{end}")
                current_user = _
                prepare_roblox = True
                current_server = server_id
        elif status in [0, 3]:
            if not prepare_roblox and current_user == _:
                prepare_roblox = True
            print(f"{user_label} is {"offline" if status == 0 else "in Roblox Studio"}.")
        elif current_server == server_id:
            print(f"{user_label} is in a game: {underline}roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}{end}")

def client_exception(error):
    global checks_since_start

    clear(False)
    print(f"{gold}[Times Checked: {checks_since_start}]{end}")
    print(error)

# If arguments are passed, close RoSniper on restart too
clear()
if "!close_after_restart" in sys.argv:
    exit()

# Save/load config file and verify it
if os.path.exists("config.json"):
    try:
        config = json.loads(open("config.json").read())
    except Exception as e:
        os.remove("config.json")
        input(f"An error occured while loading config.json: {e} ")
        os.execl(sys.executable, sys.executable, *sys.argv)
else:
    config = {}

for key in default_config.keys():
    if not key in config.keys():
        config[key] = default_config[key]
    elif type(config[key]) != type(default_config[key]):
        config[key] = default_config[key]
    if type(config[key]) == list:
        for item in range(len(config[key])):
            if type(config[key][item]) != str:
                del config[key][item]
fix_recents()
save()

# Save or add a .ROBLOSECURITY cookie
if len(config["cookies"]) == 0:
    add_account(False)

# Process args + select an account if more than one cookie is present
usernames = []
display_names = []
monitoring = False
decline_first_server = False
account_set_by_argument = False

session = requests.Session()
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg == "-m":
            monitoring = True
        elif arg == "-d":
            decline_first_server = True
        elif "-a" in arg and arg.replace("-a", "").isnumeric():
            id = int(arg[2:]) - 1
            if len(config["cookies"]) < (id + 1):
                wait(1, f"{underline}Invalid Account ID. The highest usable Account ID is {len(config["cookies"])}.{end}")
                exit()
            while len(usernames) < id:
                display_names += [""]
                usernames += [""]
            verify_cookie(id)
            if len(usernames) < (id + 1):
                wait(1, f"{underline}The selected account has an invalid cookie.{end}")
                exit()
            account_set_by_argument = True
        elif "-a" in arg and not arg.replace("-a", "").isnumeric():
            wait(1, f"{underline}Please enter a numeric Account ID.{end}")
            exit()
        else:
            continue
    sys.argv = [arg for arg in sys.argv if not arg in ("-m", "-d") and not "-a" in arg]

# Verify all .ROBLOSECURITY cookies if an account isn't set through -a
if not account_set_by_argument:
    for cookie in range(len(config["cookies"])):
        verify_cookie(cookie)
session.close()

if len(config["cookies"]) > 1 and not account_set_by_argument:
    id = float('inf')
    while len(config["cookies"]) < id:
        try:
            clear()
            print(f"{gold}[Select an Account]{end}")
            for id in range(len(usernames)):
                print(f"  - [ID: {id + 1}] {usernames[id]}")
            print("")
            id = int(input("Enter the account you want to use: ")) - 1
        except KeyboardInterrupt:
            exit()
        except:
            id = float('inf')
            wait(0.5, "Invalid ID.")
elif not account_set_by_argument:
    id = 0

if len(config["cookies"]) > 0:
    header = {
        "Cookie": f".ROBLOSECURITY={config['cookies'][id]}"
    }
else:
    os.execl(sys.executable, sys.executable, *sys.argv)

# Show main menu
while True:
    clear()
    if "!close_after_restart" in sys.argv:
        break

    if len(sys.argv) == 1:
        print(f"{gold}{bold}[RoSniper]{end}")
        print(f"Version {version}")
        print("Join-snipes accounts that the logged-in user can join!")

        print(f"{gold}\n[Tips]{end}")
        print("  - Type /cmds or /help to see the list of commands.")
        print("  - Type /changelog to see the changelog.")

        print(f"\n{gold}[Recent Users]{end}")
        for user in range(len(config["recent_users"])):
            print(f"[{user + 1}] {bold}{config["recent_users"][user]}{end}")
        if len(config["recent_users"]) == 0:
            print("No saved users! Join-snipe some users to save them to this list!")
            print(f"You can save up to {config["recent_users_length"]} users in this list{" by default. Run /set [MAX_LENGTH] to change this." if config["recent_users_length"] == 5 else "."}")
        print("")
        if decline_first_server:
            print(f"{underline}Decline First Server is Active!{end}")
        if monitoring:
            print(f"{underline}Monitoring Only Mode is Active!{end}")
        
        if usernames[id] == "Awij126":
            print(f"\033[38;5;227mLogged in as @{usernames[id]},\033[0m \033[38;5;26mwho is N00B\033[0m \033[38;5;70m(he da best noob)\033[0m")
        else:
            print(f"Logged in as {bold}{display_names[id]} (@{usernames[id]}){end}")

    try:
        if len(sys.argv) == 1:
            user = input("Enter username, recent user ID, or command: ").lower().strip()
            nl = "\n"
        else:
            user = " ".join(sys.argv[1:]).lower()
            sys.argv.append("!close_after_restart")
            nl = ""

        if user == "":
            wait(0.75, f"{underline}{nl}A user or command is required.{end}")
            if len(sys.argv) == 1:
                continue
            else:
                sys.argv.remove(-1)
    except KeyboardInterrupt:
        exit()

    # Run commands if needed
    if user.startswith("/"):
        run_command(user)
        continue

    # Check if the user enters a Recent User ID
    users = user.replace(" ", "").split(",")
    if "" in users:
        users.remove("")
    for user in range(len(users)):
        if len(users[user]) < 3 and users[user].isnumeric():
            if int(users[user]) <= len(config["recent_users"]):
                users[user] = config["recent_users"][int(users[user]) - 1].lower()
            else:
                del users
                wait(0.75, f"{underline}{nl}Recent user not avaliable.{end}")
                break

        if users[user] == usernames[id].lower() and not monitoring:
            wait(1.5, f"{underline}{nl}You can't RoSnipe yourself unless you're using the Monitoring mode.{end}")
            delete_recent_user(users[user])
            del users
            break

    if not "users" in globals():
        continue

    # Validate the username(s) provided
    try:
        data = {
            "usernames": users
        }
        req = json.loads(requests.post("https://users.roblox.com/v1/usernames/users", json=data).text)
        ids = [user["id"] for user in req["data"]]
        unames = [user["name"].lower() for user in req["data"]]

        if len(unames) != len(set(unames)):
            wait(1, f"{underline}{nl}You can't snipe the same user twice.{end}")
            continue

        faulty_users = [user for user in users if user not in unames]
        if len(faulty_users) > 0:
            [delete_recent_user(user) for user in faulty_users]
            wait(1.5, f"{underline}{nl}We searched far and wide, but these users don't exist: [@{", @".join(faulty_users)}]{end}")
            continue

        user_id_map = dict(zip(unames, ids))
        data = {
            "userIDs": [user_id_map[user] for user in users]
        }
    except Exception as e:
        if str(e) in errors.keys():
            wait(1.5, f"{underline}{errors[str(e)]}{end}")
            exit()

    # Save usernames to Recent Users
    if len(sys.argv) == 1:
        for user in users:
            delete_recent_user(user)
            config["recent_users"].insert(0, user.lower())
        fix_recents()

    # Start the RoSniper client
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
                online_data = json.loads(req.text)
                client()
                time.sleep(config["delay"])
            else:
                client_exception(f"<{req.status_code}> {errors["requests.exceptions.ConnectionError"]}")
        except requests.exceptions.ConnectionError:
            client_exception(f"{errors["requests.exceptions.ConnectionError"]} Retrying in 1s...")
            wait(1)
        except KeyboardInterrupt:
            if monitoring:
                try:
                    input("\nCTRL+C detected. Press ENTER to continue or CTRL+C again when you are done copying information. ")
                    continue
                except KeyboardInterrupt:
                    pass
            break
        except Exception as e:
            client_exception(errors[str(e)] if str(e) in errors.keys() else f"An error occured: {e} ")
            input("Press ENTER to return to the main menu. ")
            break
    session.close()
    monitoring = False
    decline_first_server = False