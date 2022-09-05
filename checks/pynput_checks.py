from pynput import keyboard

# !pip install pynput
import time
from pynput import keyboard


# print("----------------------------------------------------")
# print("Ctrl-C detected, now playing back")
# print("----------------------------------------------------")

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='C')},
    {keyboard.Key.ctrl, keyboard.KeyCode(char='c')}
]
# The currently active modifiers
current = set()

def execute():
    print ("Do Something")


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        print('alphanumericX key {0} pressed'.format(
            key.char))


    except AttributeError:
        print('special key {0} pressed'.format(
            key))
    print(f'key again {key=}')
    print([key in COMBO for COMBO in COMBINATIONS])
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()






def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
print('processing Done')




