from kivy.app import App
from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import (StringProperty, ListProperty, ObjectProperty, NumericProperty)

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
    grid_rows=NumericProperty()
    grid_cols=NumericProperty()
    grid_len=NumericProperty()
    # ScalesSelectScreen.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 1'))
    # ScalesSelectScreen.ids.button_grid.add_widget(RadioButton(text='World 3'))

    # ScreenManager.transition=RiseInTransition()
    # def populate_button(self):
    but_id_offset = 0
    button_names = [ 'button_'+ str(i+1).rjust(3,'0')[-3:] for i in range(500)]
    nbr_of_scales = len(button_names)

    def __init__(self, rows, cols):
        super(ScalesChkApp, self).__init__()
        # pass
        self.grid_rows=rows
        self.grid_cols=cols
        self.grid_len=rows*cols
        
    # def build(self):
    #     return ScreenManager()


    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)
    
    def rem_buttons(self):
        for button in self.button_matrix:
            # self.root.ids.scales_opt.remove_widget(button) 
            self.root.ids.scales_opt.ids.button_grid.remove_widget(button)
        # self.but_id_offset+=self.grid_len
    
    def scale_page(self, direction):
        if direction in ('RL','prev'):
            self.rem_buttons()
            self.but_id_offset-=self.grid_len    
            if self.but_id_offset<0:
                self.but_id_offset=0
        elif direction in ('LR', 'next'):
            self.rem_buttons()
            if self.but_id_offset+self.grid_len<self.nbr_of_scales:
                self.but_id_offset+=self.grid_len
            
        else:
            return    
        self.populate_button()
     
    def on_touch_move(self,touch):    
        if touch.dx > 0:
            self.scale_page('next')
        elif touch.dx < 0:
            self.scale_page('prev')


    def populate_button(self):
        button_matix_len=self.grid_cols*self.grid_rows
        # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 2'))
        # self.button_matrix=[]
        # for button_id in range(self.but_id_offset,self.but_id_offset+10):
        # for button_id in self.button_names:
        for button_id in self.button_names[self.but_id_offset:self.but_id_offset+self.grid_len]:
            btn = RadioButton(text=f'{button_id}')
            self.button_matrix.append(btn)
            # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text=f'auto_{button_id}'))
            self.root.ids.scales_opt.ids.button_grid.add_widget(btn)
            
        print('----------------')
    pass

#  self.manager.ids.another.ids.box.add_widget(Label(text="Button 1 pressed"))

if __name__ == '__main__':
    ScalesChkApp(14,5).run()