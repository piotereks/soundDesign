from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import StringProperty

class RadioButton(ToggleButtonBehavior, BoxLayout): 
    text = StringProperty('')
    pass

class TrackerWidget(BoxLayout):
    pass

class TrackerApp(App):

    def build(self):
        return TrackerWidget()

if __name__ == "__main__":
    TrackerApp().run()