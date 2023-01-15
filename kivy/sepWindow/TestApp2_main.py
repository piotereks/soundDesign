from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)


# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


class ScreenOne(Screen):
    pass

class ScreenTwo(Screen):
    pass

class ScreenThree(Screen):
    pass

class ScreenFour(Screen):
    pass



class Test2App(App):
    # ScreenManager.transition=RiseInTransition()
    pass



if __name__ == '__main__':
    Test2App().run()