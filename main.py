import psutil
import time
import random
import win32api
import toml
import os

# define the default key assignments
DEFAULT_KEYS = {
    "forward": "w",
    "backward": "s",
    "left": "q",
    "right": "d"
}

# create the default config file if it doesn't exist
if not os.path.exists("config.toml"):
    with open("config.toml", "w") as f:
        toml.dump({"keys": DEFAULT_KEYS}, f)

# load the config file
config = toml.load("config.toml")

# translate the letter keys to their VK codes
key_map = {}
for key, letter in config["keys"].items():
    vk_code = win32api.VkKeyScan(letter)
    key_map[key] = vk_code

# get the current time
last_interaction_time = time.time()

for p in psutil.process_iter(attrs=['pid', 'name']):
    if p.info['name'] == "VALORANT.exe":
        print((p.info['name']).upper(), "IS RUNNING!")
        while True:
            # check if the user has interacted with the keyboard
            if win32api.GetLastInputInfo() / 1000 - last_interaction_time > 240:
                # if no interaction is detected for 4 minutes, simulate keypress at random intervals
                for i in range(5):
                    time.sleep(random.uniform(0.1, 0.5))
                    win32api.keybd_event(key_map[random.choice(["forward", "backward", "left", "right"])], 0, 0, 0)
                    win32api.keybd_event(key_map[random.choice(["forward", "backward", "left", "right"])], 0, win32api.KEYEVENTF_KEYUP, 0)
                # update the last interaction time
                last_interaction_time = win32api.GetLastInputInfo() / 1000
            else:
                # if the user has interacted with the keyboard, update the last interaction time
                last_interaction_time = win32api.GetLastInputInfo() / 1000
            time.sleep(1)  # wait for 1 second before checking again
