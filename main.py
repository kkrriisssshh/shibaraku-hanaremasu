import psutil
import time
import random
import win32api
import toml
import os
import tkinter as tk
from tkinter import ttk, messagebox
import winreg

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

# create the Tkinter window
root = tk.Tk()
root.title("shibaraku-hanaremasu")
root.iconbitmap("assets/kayo.ico")
root.geometry("300x170")

# define the function that saves the new key assignments to the config file
def save_config():
    new_keys = {
        "forward": forward_entry.get(),
        "backward": backward_entry.get(),
        "left": left_entry.get(),
        "right": right_entry.get()
    }
    with open("config.toml", "w") as f:
        toml.dump({"keys": new_keys}, f)
    messagebox.showinfo("success", "key assignments saved.")

# create the entry widgets for the key assignments
tk.Label(root, text="forward:").grid(row=0, column=0, padx=5, pady=5, sticky="E")
forward_entry = ttk.Entry(root, width=5)
forward_entry.insert(0, config["keys"]["forward"])
forward_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="backward:").grid(row=1, column=0, padx=5, pady=5, sticky="E")
backward_entry = ttk.Entry(root, width=5)
backward_entry.insert(0, config["keys"]["backward"])
backward_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="left:").grid(row=2, column=0, padx=5, pady=5, sticky="E")
left_entry = ttk.Entry(root, width=5)
left_entry.insert(0, config["keys"]["left"])
left_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="right:").grid(row=3, column=0, padx=5, pady=5, sticky="E")
right_entry = ttk.Entry(root, width=5)
right_entry.insert(0, config["keys"]["right"])
right_entry.grid(row=3, column=1, padx=5, pady=5)

# create the "Save" button
save_button = ttk.Button(root, text="save", command=save_config)
save_button.grid(row=4, column=1, padx=5, pady=5, sticky="E")

def autostart_program():
    # create the registry key for autostart
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "shibaraku-hanaremasu", 0, winreg.REG_SZ, os.path.abspath("shibaraku-hanaremasu.exe"))
    messagebox.showinfo("success", "program will now start automatically on system startup.")

autostart_button = ttk.Button(root, text="enable autostart", command=autostart_program)
autostart_button.grid(row=4, column=0, padx=5, pady=5, sticky="W")

# start the Tkinter event loop
root.mainloop()

# translate the letter keys to their VK codes
key_map = {}
for key, letter in config["keys"].items():
    vk_code = win32api.VkKeyScan(letter)
    key_map[key] = vk_code

for p in psutil.process_iter(attrs=['pid', 'name']):
    if p.info['name'] == "VALORANT.exe":
        print((p.info['name']).lower(), "is running!")
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
