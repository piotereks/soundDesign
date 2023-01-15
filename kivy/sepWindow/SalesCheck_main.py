from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)


class MainScreen(Screen):
    pass

class ScalesSelectScreen(Screen):
    pass


class ScalesChkApp(App):
    # ScreenManager.transition=RiseInTransition()
    pass



if __name__ == '__main__':
    ScalesChkApp().run()