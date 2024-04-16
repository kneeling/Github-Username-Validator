import requests, threading, random, json
from setup import Fore

class Initialize:
    def __init__(self, users_file="users.txt", valid_file="valid.txt"):
        self.users_file = users_file
        self.valid_file = valid_file
        self.exists = self.read(self.valid_file)
        self.mutex = threading.Lock()

    def read(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return {line.strip() for line in file}
        except FileNotFoundError:
            return set()

    def write(self, name):
        with self.mutex:
            with open(self.valid_file, 'a') as file:
                file.write(name + '\n')
                self.exists.add(name)

    def check(self, name):
        response = requests.get(f"https://github.com/{name}")
        if response.status_code == 200:
            print(f"{Fore.YELLOW}! Name Taken: {name}")
        elif response.status_code == 404:
            if name not in self.exists:
                self.write(name)
                print(f"{Fore.GREEN}! Available: {name}")
            else:
                print(f"{Fore.RED}x Not Available (Cached): {name}")
        elif response.status_code == 429:
            print("Ratelimited waiting to retry...")
            import time
            time.sleep(random.randint(5, 15))
            return False
        else:
            print(f"{Fore.RED}x Name Check err for {name}: HTTP {response.status_code}")
        return True

    def main(self, usernames):
        for name in usernames:
            success = False
            while not success:
                success = self.check(name)

def run():
    with open("config.json", "r") as conf:
        config = json.load(conf)

    instance = Initialize()
    with open(instance.users_file, 'r') as file:
        usernames = [line.strip() for line in file if line.strip()]

    num_threads = config["threads"]
    threads = []
    usernames_per_thread = len(usernames) // num_threads
    for i in range(num_threads):
        start_index = i * usernames_per_thread
        if i == num_threads - 1:
            end_index = len(usernames)
        else:
            end_index = start_index + usernames_per_thread
        thread_usernames = usernames[start_index:end_index]
        thread = threading.Thread(target=instance.main, args=(thread_usernames,))
        thread.daemon = True
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

run()
