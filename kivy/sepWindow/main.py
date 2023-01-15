from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

class HomeScreen(BoxLayout):
    pass

class Screen1(Screen):
    pass

class SplitScreenApp(App):
    def build(self):

        return HomeScreen()

if __name__ == "__main__":
    SplitScreenApp().run()