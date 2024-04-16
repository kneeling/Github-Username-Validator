import os, sys, time, json
from colorama import *
class Setup:
    def __init__(self):
        self.check("users.txt")
        self.check("valid.txt")
        self.check("config.json")
        self.update()

    def check(self, filename):
        if os.path.exists(filename):
            print(f"[{Fore.LIGHTGREEN_EX}*{Fore.RESET}] Found {filename}")
        else:
            with open(filename, "w") as file:
                print(f"[{Fore.LIGHTYELLOW_EX}!{Fore.RESET}] Created {filename}")
        time.sleep(1)

    def update(self):
        default_config = {
            "random_users": False,
            "threads": 100,
            "delay": 0
        }

        config = "config.json"

        try:
            if os.path.exists(config):
                with open(config, "r") as config_file:
                    config_open = json.load(config_file)
            else:
                config_open = {}

            for key, value in default_config.items():
                config_open.setdefault(key, value)

            with open(config, "w") as config_f:
                json.dump(config_open, config_f, indent=4)
                if os.path.exists(config):
                    print(f"[{Fore.LIGHTGREEN_EX}*{Fore.RESET}] Found config.json")
                else:
                    print(f"[{Fore.LIGHTGREEN_EX}*{Fore.RESET}] Created config.json")

        except (OSError, IOError) as e:
            print(f"[{Fore.RED}ERROR{Fore.RESET}] Failed to update config.json: {e}")
