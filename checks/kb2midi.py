# !pip install pynput
import time
from pynput import keyboard

def on_press(key):
  print("press:",key)
    # if any([key in COMBO for COMBO in COMBINATIONS]):
    #     current.add(key)
    #     if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
    #         print("Ctrl+Cq pressed")

def on_release(key):
  print("rel:",key)
    # if any([key in COMBO for COMBO in COMBINATIONS]):
    #     current.remove(key)


def tst():
  COMBINATIONS = [
      {keyboard.Key.ctrl, keyboard.KeyCode(char='c')}
  ]

  current = set()

  with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
      listener.join()

try:
    while True:
        time.sleep(1)
        print(time.time())
        pass
except KeyboardInterrupt:
    pass

print("----------------------------------------------------")
print("Ctrl-C detected, now playing back")
print("----------------------------------------------------")