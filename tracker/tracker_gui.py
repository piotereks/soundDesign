from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import StringProperty, ListProperty


class RadioButton(ToggleButtonBehavior, BoxLayout): 
    text = StringProperty('')
    pass

class TrackerWidget(BoxLayout):
    pass

class TrackerApp(App):
    scale_init_text = StringProperty()
    scale_values = ListProperty()

    # def on_touch_down(self, touch):
    #     if touch.is_mouse_scrolling:
    #         if touch.button == 'scrolldown':
    #             print('down')
    #         elif touch.button == 'scrollup':
    #             print('up')
    #     TrackerWidget.on_touch_down(self, touch)
    
    
    def build(self):
        return TrackerWidget()

if __name__ == "__main__":
    TrackerApp().run()