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
from pathlib import Path
from platformdirs import user_config_dir

op = platform.system()
if op == "Windows":
    import subprocess

if getattr(sys, 'frozen', False):
    if len(sys.argv) >= 2 and sys.argv[0] == sys.argv[1]:
        sys.argv.pop(1)

version = "2.0.0"
os.chdir(os.path.dirname(__file__))

config_dir = Path(user_config_dir("RoSniper", "introvertednoob"))
config_dir.mkdir(parents=True, exist_ok=True)
config_path = f"{config_dir}/config.json"

gold = "\033[0;33m"
bold = "\033[1m"
underline = "\033[4m"
end = "\033[0m"

errors = {
    "requests.exceptions.ConnectionError": "[ConnectionError] Couldn't connect to the Roblox servers.",
    "requests.exceptions.ConnectTimeout": "[ConnectTimeout] Your request with the Roblox servers timed out.",
    "requests.exceptions.SSLError": "[SSLError] Couldn't connect to the Roblox servers. Your internet may be blocking Roblox.",
    "requests.exceptions.ReadTimeout": "[ReadTimeout] Your request with the Roblox servers timed out."
}

default_config = {
    "recent_users_length": 5,
    "delay": 0.01,
    "show_tips": True,
    "verify_method": "prog",
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
    with open(config_path, "w", encoding="utf-8") as cfg:
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
        cj = getattr(browser_cookie3, browser)(domain_name="roblox.com")
        for cookie in cj:
            if cookie.name == ".ROBLOSECURITY":
                return cookie.value
        return None
    except Exception as e:
        print(f"Error reading cookies: {e}")
        return None

def check_cookie(cookie):
    global session
    global valid_accounts

    if cookie["username"] in valid_accounts and config["verify_method"] == "prog":
        return True

    header = {
        "Cookie": f".ROBLOSECURITY={cookie["cookie"]}"
    }

    times_verified = 0
    while True:
        try:
            req = session.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers=header)
            if not req.ok:
                return False
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            err = f"{type(e).__module__}.{type(e).__name__}"
            
            clear()
            print(f"{gold}[RoSniper has encountered an error!]{end}")
            if err in errors.keys():
                print(errors[err])
                print(f"{bold}There is likely an issue with your network or Roblox's servers.{end}")
            else:
                print(f"An error has occured: {err}")
            input(f"\nFull Error:\n{str(e)}")
            exit()

        cid = config["cookies"].index(cookie)
        if req.ok:
            if config["verify_method"] == "prog":
                valid_accounts += [cookie["username"]]

            correct_uname = json.loads(req.text)["name"]
            correct_dname = json.loads(req.text)["displayName"]
            if config["cookies"][cid]["username"] != correct_uname or config["cookies"][cid]["display_name"] != correct_dname:
                config["cookies"][cid]["username"] = correct_uname
                config["cookies"][cid]["display_name"] = correct_dname
                if config["verify_method"] != "all":
                    usernames[cid] = config["cookies"][cid]["username"]
                    display_names[cid] = config["cookies"][cid]["display_name"]
                save()

            return True
        elif req.status_code == 429:
            clear()
            print(f"{gold}[Network Error - Too Many Requests]{end}")
            print(f"Couldn't contact the Roblox servers to authenticate you.")
            print("RoSniper will keep trying to verify your account every 5 seconds.")
            print(f"\nAttempted to verify this account {times_verified} time(s)")
            print("This only counts the attempts after this error was received.")
            print(f"\nCurrently trying to verify account: @{config["cookies"][cid]["username"]}")
            wait(5, f"Account ID: {cid + 1} (of {len(config["cookies"])})")
            times_verified += 1
        else:
            return False

def replace_cookie(cid):
    clear()
    print(f"{gold}[Invalid Cookie]{end}")
    print(f"The cookie associated with {bold}the account @{config["cookies"][cid]["username"]}{end} is invalid.")
    print(f"\n{underline}To resolve this issue, you can:{end}")
    print("    - Type 'y' to replace the old cookie while keeping it in the same position")
    print("    - Press ENTER to remove the cookie\n")
    readd_account = input("Choose an option: ").lower().strip().startswith("y")

    if readd_account:
        add_account(mode="replace", cid=cid)
    else:
        config["cookies"].remove(config["cookies"][i])
        save()
        set_account()

def add_account(mode="add", cid=None):
    global usernames
    global display_names

    clear()
    print(f"{gold}{"[Add Account]" if mode == "add" else "[Replace Cookie]"}{end}")
    print(f"{bold}Copy a .ROBLOSECURITY cookie to your clipboard.{f" It must belong to @{config["cookies"][cid]["username"]}." if mode == "replace" else ""}{end}")
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

    try:
        req = requests.get("https://users.roblox.com/v1/users/authenticated", timeout=5, headers={"Cookie": f".ROBLOSECURITY={cookie}"})
        if not req.ok:
            pyperclip.copy("")
            input("\nInvalid cookie. Restart RoSniper to try again. ")
            exit()

        cookie_dict = {
            "cookie": cookie,
            "username": json.loads(req.text)["name"],
            "display_name": json.loads(req.text)["displayName"]
        }

        if cookie_dict in config["cookies"] and mode == "add":
            pyperclip.copy("")
            input("\nThis cookie already exists. ")
            return

        if mode == "add":
            config["cookies"] += [cookie_dict]
            usernames += [cookie_dict["username"]]
            display_names += [cookie_dict["display_name"]]
        else:
            if cookie_dict["username"] == config["cookies"][cid]["username"]:
                config["cookies"][cid] = cookie_dict
            else:
                input("\nThis cookie doesn't match the right account. Restart RoSniper to try again. ")
                exit()

        save()
        pyperclip.copy("")
        input(f"\nCookie saved successfully. Welcome, {json.loads(req.text)["name"]}! ")
    except Exception as e:
        err = f"{type(e).__module__}.{type(e).__name__}"
        if err in errors.keys():
            input(f"\n{errors[err]} ")
        else:
            clear()
            input(f"An error has occured: {err} ")
        exit()

def set_account(cid=None):
    global id
    global header
    global account_set_by_argument

    if cid != None:
        if config["verify_method"].startswith("prog") and not account_set_by_argument:
            if not check_cookie(config["cookies"][cid]):
                replace_cookie(cid)

        id = cid
        header = {
            "Cookie": f".ROBLOSECURITY={config["cookies"][id]["cookie"]}"
        }
        return

    if len(config["cookies"]) > 1 and (not account_set_by_argument or not (account_set_by_argument and config["verify_method"] == "none")):
        id = ""
        while id not in range(0, len(config["cookies"])):
            try:
                clear()
                print(f"{gold}[Account Selection]{end}")
                for id, username in enumerate(usernames, start=1):
                    print(f"  - [ID: {id}] {username}")

                id = input("\nEnter the account you want to use: ").strip()
                if not id.isdecimal() or id == "0":
                    wait(0.5, "Invalid ID.")
                    continue
                id = int(id) - 1

                if id >= len(config["cookies"]):
                    wait(0.5, "Invalid ID.")

                if config["verify_method"].startswith("prog"):
                    if not check_cookie(config["cookies"][id]):
                        replace_cookie(id)
            except KeyboardInterrupt:
                exit()            
    elif not account_set_by_argument:
        id = 0

def run_command(command):
    global usernames
    global display_names
    global monitoring
    global decline_first_server

    arg = command.split(" ")[1] if len(command.split(" ")) > 1 else ""
    if command in ["/help", "/cmds", "/changelog"]:
        clear()
        load_file = f"./assets/{"commands" if command in ["/help", "/cmds"] else "changelog"}.txt"
        if os.path.exists(load_file):
            print(open(load_file).read().format(
                green="\033[0;32m",
                gold=gold,
                bold=bold,
                underline=underline,
                end=end,
                cur_recent_users=config["recent_users_length"],
                cur_delay=config["delay"],
                cur_df=decline_first_server,
                cur_m=monitoring,
                cur_tips=config["show_tips"],
                cur_method=config["verify_method"]
            ))
            input("Press ENTER to return to the main menu. ")
        else:
            wait(1, f"The file {load_file} isn't present.")
    elif command.startswith("/setrecents ") or command.startswith("/set "):
        if arg.isdecimal():
            config["recent_users_length"] = 99 if int(arg) > 99 else int(arg)
            fix_recents()
            wait(1, f"{nl}{underline}Set the length of Recent Users to {config["recent_users_length"]}{" (max)" if config["recent_users_length"] > 99 else ""}.{end}")
        else:
            wait(1, f"{nl}{underline}Invalid length.{end}")
        save()
    elif command.startswith("/del "):
        if config["recent_users"] == []:
            wait(0.75, f"{nl}{underline}There are no Recent Users to delete.{end}")
        elif arg == "*":
            config["recent_users"] = []
        elif arg in config["recent_users"]:
            config["recent_users"].remove(arg)
        elif arg.isdecimal():
            if int(arg) <= len(config["recent_users"]):
                del config["recent_users"][int(arg) - 1]
            else:
                wait(0.75, f"{nl}{underline}This Recent User doesn't exist.{end}")
        else:
            wait(0.75, f"{nl}{underline}This Recent User doesn't exist.{end}")
        save()
    elif command.startswith("/logout"):
        if arg == "":
            del config["cookies"][id]
            del usernames[id]
            del display_names[id]
            print(f"{nl}{underline}Deleted this account's cookie from config.json.{end}")
        elif arg == "*":
            config["cookies"] = []
            usernames = []
            display_names = []
            print(f"{nl}{underline}Removed all cookies from config.json.{end}")
        else:
            wait(2, f"{nl}{underline}Invalid argument. See /cmds for proper documentation.{end}")
            return

        save()
        if len(config["cookies"]) == 0:
            wait(1.5, f"{bold}You'll be redirected to the Add Account menu.{end}")
            add_account()
        else:
            wait(1.5, f"{bold}You'll be redirected to the Set Account menu.{end}")
            set_account()
    elif command in ["/addaccount", "/add"]:
        wait(1, f"{nl}{underline}You will be redirected to the Add Account menu.{end}")
        add_account()
        set_account()
    elif command.startswith("/delay "):
        config["delay"] = float(arg) if arg.replace(".", "").isnumeric() else 0.01
        save()
        wait(0.5, f"{nl}{underline}Delay set to {config["delay"]}s.{end}")
    elif command.startswith("/switch") or command.split(" ")[0] == "/s":
        serialized_users = [user.lower() for user in usernames]

        if account_set_by_argument and config["verify_method"] == "all":
            wait(4, f"{nl}You have selected your account using -a, which only verifies that account's cookie.\n{underline}Therefore, you cannot use the /switch command.{end}\nRun /setVerify prog OR /setVerify none to bypass this.")
            return
        elif len(config["cookies"]) == 1:
            wait(1.5, f"{nl}{underline}You don't have any other accounts to switch to.{end}")
            return

        if arg == "":
            wait(1, f"{nl}{underline}You will be redirected to the Account Selection menu.{end}")
            set_account()
        elif arg.isdecimal():
            cid = int(arg) - 1
            if cid == id:
                wait(1, f"{nl}{underline}You are already using the @{usernames[id]} account.{end}")
                return

            if (cid + 1) > len(config["cookies"]) or cid == -1:
                wait(0.75, f"{nl}{underline}This Account ID is invalid.{end}")
                return

            set_account(cid)
        elif arg in serialized_users:
            if arg == usernames[id].lower():
                wait(1, f"{nl}{underline}You are already using the @{usernames[id]} account.{end}")
                return

            set_account(serialized_users.index(arg))
        else:
            wait(1, f"{nl}{underline}Invalid argument. See /cmds for proper documentation.{end}")
            return
    elif command in ["/df", "/declinefirst"]:
        monitoring = False
        decline_first_server = False if decline_first_server else True
    elif command in ["/m", "/monitoring"]:
        decline_first_server = False
        monitoring = False if monitoring else True
    elif command == "/alias":
        if not op == "Darwin":
            wait(1, f"{nl}{underline}You must be using macOS to run this command.{end}")
            return

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
            wait(1, f"\n{underline}Successfully added the <snipe> alias.{end}")
        else:
            if not "alias snipe=" in open(f"/Users/{getpass.getuser()}/.zshrc").read():
                open(f"/Users/{getpass.getuser()}/.zshrc", "a").write(f"\n{snipe_alias}")
            else:
                zshrc = open(f"/Users/{getpass.getuser()}/.zshrc").readlines()
                for line in range(len(zshrc)):
                    if "alias snipe=" in zshrc[line]:
                        zshrc[line] = snipe_alias + "\n"

                open(f"/Users/{getpass.getuser()}/.zshrc", "w").writelines(zshrc)
                wait(1, f"\n{underline}Successfully updated the <snipe> alias.{end}")
                return
    elif command.startswith("/donate "):
        if not os.path.exists("./assets/donations.json"):
            wait(1, f"{nl}{underline}The file ./assets/donations.json isn't present.{end}")
            return

        donations = json.loads(open("./assets/donations.json").read())
        if arg in donations.keys():
            print(f"{nl}{underline}Thank you for donating! Donations help keep RoSniper free for all! - @Awij126{end}")
            wait(3, f"A gamepass for {bold}{arg} Robux{end} will open shortly.")
            webbrowser.open(f"https://www.roblox.com/game-pass/{donations[arg]}")
        else:
            wait(1, f"{nl}{underline}Invalid donation amount. See /cmds for valid donation amounts.{end}")
    elif command == "/toggletips":
        config["show_tips"] = False if config["show_tips"] else True
        save()
    elif command.startswith("/setverify") or command.startswith("/sv"):
        if arg == config["verify_method"]:
            wait(0.75, f"{nl}{underline}This verification method is already being used.{end}")
        elif arg in ["prog", "prog-nocache", "all", "none"]:
            config["verify_method"] = arg
            save()
            wait(0.75, f"{nl}{underline}Successfully changed the cookie verification method.{end}")
        else:
            wait(1, f"{nl}{underline}Invalid cookie verification method. See /cmds for valid arguments.{end}")
    else:
        similar_commands = []
        list_of_commands = ["/add", "/addaccount", "/alias", "/cmds", "/changelog", "/delay", "/del", "/df", "/declinefirst", "/donate", "/help", "/m", "/monitoring", "/logout", "/s", "/set", "/setrecents", "/setverify", "/sv", "/switch", "/toggletips"]
        for cmd in list_of_commands:
            if command in cmd or cmd in command:
                similar_commands += [cmd]
        if len(similar_commands) == 0 or similar_commands == list_of_commands:
            wait(2, f"{nl}{underline}Invalid command: \"{command}\"{end}\nType /cmds to see documentation on commands.")
        elif command in list_of_commands:
            wait(2, f"{nl}{underline}This command exists, but it requires arguments.{end}\nType /cmds to see documentation on the arguments for commands.")
        else:
            wait(2 + (0.25 * len(similar_commands)), f"{nl}{underline}Invalid command: \"{command}\". Perhaps you meant \"{"\", \"".join(similar_commands)}\"?{end}\nType /cmds to see documentation on commands.")

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

    for i, user in enumerate(users):
        status = online_data["userPresences"][i]["userPresenceType"]
        place_id = online_data["userPresences"][i]["placeId"]
        server_id = online_data["userPresences"][i]["gameId"]
        user_label = f"{bold + "[Priority] " + end if i == current_user and not monitoring else ""}{user}"

        if status == 1:
            if i == current_user and prepare_roblox and not monitoring:
                if op == "Darwin":
                    open_link("roblox://")
                else:
                    subprocess.run(["taskkill", "/f", "/im", "RobloxPlayerBeta.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                current_server = ""
                prepare_roblox = False
            print(f"{user_label} is on the Roblox website!")
        elif status == 2 and place_id == server_id == None:
            print(f"{user_label} has their joins off, or you aren't following them.")
            print(f"   -> Follow them @ https://roblox.com/users/{data["userIDs"][i]}/profile")
            print("   -> This screen will automatically update when you follow/friend the user.")
        elif status == 2 and current_server != server_id:
            if decline_first_server and i == current_user:
                declined_servers += [server_id]
                decline_first_server = False

            if server_id in declined_servers:
                print(f"{user_label} is in a server you declined (roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}).")
                continue
            elif current_user != i and not monitoring:
                if input(f"\n{user} is in a game, but you are focusing on {users[current_user]}.\nPress ENTER to focus on {user}, or type 'q' to decline. ").lower().strip().startswith("q"):
                    print(f"Declined to join {user}. RoSniper will still check for {user}, but won't show you that server.")
                    declined_servers += [server_id]

                    if input(f"   -> Would you like to focus on {user}, so you can join them next time (y/n)? ").lower().strip().startswith("y"):
                        current_user = i

            if not server_id in declined_servers:
                if not monitoring:
                    open_link(f'roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}')
                print(f"{user_label} is in a game: {underline}roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}{end}")
                current_user = i
                prepare_roblox = True
                current_server = server_id
        elif status in [0, 3]:
            if not prepare_roblox and current_user == i:
                prepare_roblox = True
            print(f"{user_label} is {"offline" if status == 0 else "in Roblox Studio"}.")
        elif current_server == server_id:
            print(f"{user_label} is in a game: {underline}roblox://experiences/start?placeId={place_id}&gameInstanceId={server_id}{end}")

def client_exception(error):
    global checks_since_start

    clear(False)
    print(f"{gold}[Times Checked: {checks_since_start}]{end}")
    print(error)

# if arguments are passed, close RoSniper on restart
clear()
if "!close_after_restart" in sys.argv:
    exit()

# save/load config file and verify it
if os.path.exists(config_path):
    try:
        config = json.loads(open(config_path).read())
    except Exception as e:
        os.remove(config_path)
        input(f"An error occured while loading config.json: {e} ")
        os.execl(sys.executable, sys.executable, *sys.argv)
else:
    config = {}

for key in default_config.keys():
    if not key in config.keys():
        config[key] = default_config[key]
    elif not isinstance(config[key], type(default_config[key])):
        config[key] = default_config[key]
    
    if isinstance(config[key], (int, float)):
        if config[key] < 0:
            config[key] = default_config[key]
    elif isinstance(config[key], list) and key == "recent_users":
        config[key] = [item for item in config[key] if isinstance(item, str)]
    elif isinstance(config[key], list) and key == "cookies":
        config[key] = [item for item in config[key] if isinstance(item, object)]
        required = {"cookie", "username", "display_name"}

        marked_for_deletion = []
        for cookie in config[key]:
            if not required.issubset(cookie):
                marked_for_deletion.append(cookie)
        for cookie in marked_for_deletion:
            del config[key][config[key].index(cookie)]
fix_recents()
save()

# save or add a .ROBLOSECURITY cookie
if len(config["cookies"]) == 0:
    add_account()

usernames = []
display_names = []
valid_accounts = []
monitoring = False
decline_first_server = False
account_set_by_argument = False

# process args
session = requests.Session()
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg == "-m":
            monitoring = True
            decline_first_server = False
        elif arg == "-d":
            decline_first_server = True
            monitoring = False
        elif arg.startswith("-a") and arg.replace("-a", "").isdecimal():
            id = int(arg[2:]) - 1
            if len(config["cookies"]) < (id + 1):
                wait(1, f"{underline}Invalid Account ID. The highest usable Account ID is {len(config["cookies"])}.{end}")
                exit()

            account_set_by_argument = True
            set_account(id)
        elif "-a" in arg and not arg.replace("-a", "").isdecimal():
            wait(1, f"{underline}Please enter a numeric Account ID.{end}")
            exit()
        else:
            continue
    sys.argv = [arg for arg in sys.argv if not arg in ("-m", "-d") and not arg.startswith("-a")]

# verify cookies depending on the method chosen
for i, cookie in enumerate(config["cookies"][:]):
    if account_set_by_argument and i == id:
        if not check_cookie(config["cookies"][i]):
            wait(1, f"{underline}The selected account has an invalid cookie.{end}")
            exit()
    if config["verify_method"] == "all" and not account_set_by_argument:
        if check_cookie(cookie):
            display_names += [cookie["display_name"]]
            usernames += [cookie["username"]]
        else:
            replace_cookie(i)
    else:
        display_names += [cookie["display_name"]]
        usernames += [cookie["username"]]
if not account_set_by_argument:
    set_account()
session.close()

if len(config["cookies"]) > 0:
    header = {
        "Cookie": f".ROBLOSECURITY={config["cookies"][id]["cookie"]}"
    }
else:
    add_account()

# set this to your Roblox username to see some easter eggs!
easter_egg_user = "Awij126"
while True:
    clear()
    if "!close_after_restart" in sys.argv:
        break

    if len(sys.argv) == 1:
        print(f"{gold}{bold}[RoSniper]{end}")
        print(f"Version {version} ({"binary" if getattr(sys, 'frozen', False) else "source"})")
        print("Join-snipes accounts that the logged-in user can join!")
        print(f"Cookie verification method: {config["verify_method"].replace("prog", "progressive")}")

        if config["show_tips"] == True:
            print(f"{gold}\n[Tips]{end}")
            print("  - Type /help or /cmds to see the list of commands.")
            print("  - Type /changelog to see the changelog.")
            print("  - Type /toggletips to hide or show these tips.")

        print(f"\n{gold}[Recent Users]{end}")
        for user in range(len(config["recent_users"])):
            print(f"[{user + 1}] {bold}{config["recent_users"][user]}{end}")
        
        if len(config["recent_users"]) == 0 and config["show_tips"]:
            print("No saved users! Join-snipe some users to save them to this list!")
            print(f"You can save up to {config["recent_users_length"]} users in this list{" by default. Run /set [MAX_LENGTH] to change this." if config["recent_users_length"] == 5 else "."}")
        elif len(config["recent_users"]) == 0:
            print("No saved users!")

        print("")
        if decline_first_server:
            print(f"{underline}Decline First Server is Active!{end}")
        if monitoring:
            print(f"{underline}Monitoring Only Mode is Active!{end}")
        
        if usernames[id].lower() == easter_egg_user.lower():
            print(f"\033[38;5;227mLogged in as @{usernames[id]},\033[0m \033[38;5;26mwho is N00B\033[0m \033[38;5;70m(he da best noob)\033[0m")
        else:
            print(f"Logged in as {bold}{display_names[id]} (@{usernames[id]}){end}")

    try:
        if len(sys.argv) == 1:
            user = input(f"Enter a username, recent user ID, or command{", hax0r" if usernames[id].lower() == easter_egg_user.lower() else ""}: ").lower().strip()
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

    # run commands
    try:
        if user.startswith("/"):
            run_command(user)
            continue
    except KeyboardInterrupt:
        exit()

    # check if the user enters a recent User ID
    users = user.replace(" ", "").split(",")
    if "" in users:
        users.remove("")
    for i, user in enumerate(users):
        if len(user) < 3 and user.isdecimal():
            if int(user) <= len(config["recent_users"]):
                users[i] = config["recent_users"][int(user) - 1].lower()
            else:
                del users
                wait(0.75, f"{underline}{nl}Recent user not avaliable.{end}")
                break

        if user == usernames[id].lower() and not monitoring:
            wait(1.5, f"{underline}{nl}You can't RoSnipe yourself unless you're using the Monitoring mode.{end}")
            delete_recent_user(user)
            del users
            break

    if not "users" in globals():
        continue

    # validate usernames
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
        err = f"{type(e).__module__}.{type(e).__name__}"
        if err in errors.keys():
            wait(1.5, f"{underline}{errors[err]}{end}")
            exit()
        else:
            wait(1.5, f"{underline}An error has occured: {err}{end}")

    # save usernames to Recent Users
    if len(sys.argv) == 1:
        for user in users:
            delete_recent_user(user)
            config["recent_users"].insert(0, user.lower())
        fix_recents()

    # start the RoSniper client
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
            err = f"{type(e).__module__}.{type(e).__name__}"
            client_exception(errors[err] if err in errors.keys() else f"An error has occured: {err}")
            input("Press ENTER to return to the main menu. ")
            break
    session.close()
    monitoring = False
    decline_first_server = False