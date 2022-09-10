from pynput import keyboard

# !pip install pynput
import time
from pynput import keyboard


global prev_key
prev_key = None


def on_press(key):
    global prev_key
    if not prev_key:
        prev_key = key
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
            note = play_keys.index(key.char)+60 if key.char in play_keys else None
            print(f'{note=}')

        except AttributeError:
            print('special key {0} pressed'.format(
                key))



def on_release(key):
    global prev_key
    print('{0} released'.format(
        key))
    prev_key = None
    if key == keyboard.Key.esc:
        # Stop listener
        return False

play_keys = "q2w3er5t6y7ui9o0p[=]"
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




