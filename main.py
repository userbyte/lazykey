## lazykey
## 10/16/2022
## Written by userbyte
## Description: key-holder for lazy cunts

version = '0.1.2.7'
print('''
 ____ ____ ____ 
||L |||Z |||K ||
||__|||__|||__||
|/__\|/__\|/__\|
''')
print(f'starting lazykey v{version}')

from pynput import keyboard
from time import sleep
import pyautogui # need to use this because pynput no longer works to hold keys for some reason, but its fine
import signal

kb = keyboard.Controller()

global keys
global keyhold
global curheld
keys = []
keyhold = False
curheld = []

def signal_handler(signal, frame):
    print(f'Signal (ID: {signal}) has been caught. Exiting...')
    #keyboard.Listener.stop() # doesnt work cuz needs self idk
    #print('Keyboard listener stopped')
    exit()
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def add_to_keylist(k):
    global keys
    if type(k) == type(str()): k = k.lower() # make lowercase to prevent adding 2 of the same key to the list (ex. ['W', 'w', 'E', 'e'])
    if k in keys: pass
    else: keys.append(k)

def remove_from_keylist(k):
    global keys
    try: keys.remove(k)
    except ValueError: pass # we dont really care if it wasnt in the list

def toggle_keyhold():
    global keyhold
    global curheld
    if keyhold == True:
        keyhold = False
        print(f'keyhold now {keyhold}')
        for k in curheld:
            print(f'kh: released {k}')
            # kb.release(k)
            pyautogui.keyUp('w')
            curheld.remove(k)
    elif keyhold == False:
        if len(keys) == 0:
            print('kh: no keys are in the keylist, not doing keyhold')
            return
        keyhold = True
        print(f'keyhold now {keyhold} (with keys: {keys})')
        print('kh: please let go of the keys within the next 5 seconds or this wont work')
        sleep(5)
        print('kh: ok, doing the thing...')
        for k in keys:
            print(f'kh: pressing {k}')
            # kb.press(k)
            pyautogui.keyDown('w')
            curheld.append(k)

def on_press(key):
    global keys
    if key == keyboard.Key.f7:
        # [F7] toggles keyholding
        toggle_keyhold()
        return
    if key in curheld:
        print(f'{key} IN CURHELD')
    try:
        #print(f'Alphanumeric key pressed: {key.char}')
        add_to_keylist(key.char)
    except AttributeError:
        #print(f'Special key pressed: {key.name}')
        add_to_keylist(key.name)
    print(f'keylist: {keys}')

def on_release(key):
    global keys
    global curheld
    if key == keyboard.Key.f6:
        # [F6] stops listener
        print('Stopping')
        return False
    if key in curheld: print(f'{key} IN CURHELD')
    try:
        #print(f'Alphanumeric key released: {key.char}')
        remove_from_keylist(key.char)
    except AttributeError:
        #print(f'Special key released: {key.name}')
        remove_from_keylist(key.name)
    print(f'keylist: {keys}')

print('starting listener')
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
print('exiting')