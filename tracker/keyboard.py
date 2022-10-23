from pynput import keyboard


class Keyboard:

    def __init__(self, function : callable = lambda x: print(x)):
        self.prev_key = None
        self.note = None
        self.play_keys = "q2w3er5t6y7ui9o0p[=]"
        self.func_on_note = function
        # self.func_on_note()
        self.start_listerner(self)

    def on_press(self, key):
        if not self.prev_key:
            self.prev_key = key
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
                if key.char in self.play_keys:
                    self.note = self.play_keys.index(key.char)+60
                    self.func_on_note(self.note)

            except AttributeError:
                print('special key {0} pressed'.format(key))

    def on_release(self, key):
        print('{0} released'.format(key))
        self.prev_key = None
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    @staticmethod
    def start_listerner(self):
        # Collect events until released
        # with keyboard.Listener(
        #         on_press=self.on_press,
        #         on_release=self.on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()
        print('listener started')

def xxx(x):
    print("asdfadf1111-:", x)
def main():
    Keyboard(lambda x : xxx(x))


if __name__ == "__main__":
    main()

