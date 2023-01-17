from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import StringProperty, ListProperty, ObjectProperty

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
    btn = ObjectProperty()
    button_matrix = ListProperty()
    # ScalesSelectScreen.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 1'))
    # ScalesSelectScreen.ids.button_grid.add_widget(RadioButton(text='World 3'))

    # ScreenManager.transition=RiseInTransition()
    # def populate_button(self):
    but_id_offset = 0

    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)
    
    def rem_buttons(self):
        for button in self.button_matrix:
            # self.root.ids.scales_opt.remove_widget(button) 
            self.root.ids.scales_opt.ids.button_grid.remove_widget(button)
        self.but_id_offset+=100
    
    def populate_button(self):
        self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 2'))
        # self.button_matrix=[]
        for button_id in range(self.but_id_offset,self.but_id_offset+10):
            btn = RadioButton(text=f'auto_{button_id}')
            self.button_matrix.append(btn)
            # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text=f'auto_{button_id}'))
            self.root.ids.scales_opt.ids.button_grid.add_widget(btn)
            
        print('----------------')
    pass

#  self.manager.ids.another.ids.box.add_widget(Label(text="Button 1 pressed"))

if __name__ == '__main__':
    ScalesChkApp().run()