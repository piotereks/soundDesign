from pynput import keyboard
from log_call import *

class Keyboard:

    def __init__(self, function : callable = lambda x: print(x)):
        self.prev_key = None
        self.note = None
        self.play_keys = "q2w3er5t6y7ui9o0p[=]"
        self.control_keys = "zxcvbnm"
        self.func_on_note = function
        # self.func_on_note()
        # self.start_listerner(self)
        self.start_kb_listener(self)

    def key_z_function(self):
        log_call()

    def key_x_function(self):
        log_call()

    def key_c_function(self):
        log_call()

    def key_v_function(self):
        log_call()

    def key_b_function(self):
        log_call()

    def key_n_function(self):
        log_call()

    def key_m_function(self):
        log_call()


    def on_press(self, key):
        if not self.prev_key:
            self.prev_key = key
            try:
                print('alphanumeric key {0} pressed'.format(key.char))
                if key.char in self.play_keys:
                    self.note = self.play_keys.index(key.char)+60
                    self.func_on_note(self.note)
                elif key.char in self.control_keys:
                    key_function = getattr(self, "key_"+key.char+"_function")
                    key_function()

            except AttributeError:
                print('special key {0} pressed'.format(key))



    def on_release(self, key):
        print('{0} released'.format(key))
        self.prev_key = None
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    @staticmethod
    def start_kb_listener(self):
        # Collect events until released
        # with keyboard.Listener(
        #         on_press=self.on_press,
        #         on_release=self.on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()
        print('listener started')


    def stop_listener(self):
        self.listener.stop()

    def start_listener(self):
        self.listener.start()



def xxx(x):
    print("asdfadf1111-:", x)
def main():
    xxx = Keyboard(lambda x : print("key preseed: " +str(x)))




if __name__ == "__main__":
    main()

