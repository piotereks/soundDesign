from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import StringProperty, ListProperty

class MainScreen(Screen):

    pass

class ScalesSelectScreen(Screen):
    # def on_start(self):
    # ScalesSelectScreen.ids.button_grid.add_widget(RadioButton(text='World 2'))

    pass

class RadioButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    pass


class ScalesChkApp(App):
    selected_scale_button = StringProperty()
    # ScalesSelectScreen.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 1'))
    # ScalesSelectScreen.ids.button_grid.add_widget(RadioButton(text='World 3'))

    # ScreenManager.transition=RiseInTransition()
    # def populate_button(self):
    
    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)
    
    def on_start(self):
        self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 2'))
        for button_id in range(10):
            self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text=f'auto_{button_id}'))
            
        print('----------------')
    pass

#  self.manager.ids.another.ids.box.add_widget(Label(text="Button 1 pressed"))

if __name__ == '__main__':
    ScalesChkApp().run()