import psutil
import time
import random
import win32api

keys = [0x5A, 0x51, 0x53, 0x44] # define a list of keys to simulate keypress
last_interaction_time = time.time() # get the current time

for p in psutil.process_iter(attrs=['pid', 'name']): 
    if p.info['name'] == "VALORANT.exe": 
        print((p.info['name']).upper(), "IS RUNNING!")
        while True:
            # check if the user has interacted with the keyboard
            if win32api.GetLastInputInfo() / 1000 - last_interaction_time > 240:
                # if no interaction is detected for 4 minutes, simulate keypress at random intervals
                for i in range(5):
                    time.sleep(random.uniform(0.1, 0.5))
                    win32api.keybd_event(random.choice(keys), 0, 0, 0)
                    win32api.keybd_event(random.choice(keys), 0, win32api.KEYEVENTF_KEYUP, 0)
                # update the last interaction time
                last_interaction_time = win32api.GetLastInputInfo() / 1000
            else:
                # if the user has interacted with the keyboard, update the last interaction time
                last_interaction_time = win32api.GetLastInputInfo() / 1000
            time.sleep(1)  # wait for 1 second before checking again
    else:
        print((p.info['name']).upper(), "IS NOT RUNNING!")
