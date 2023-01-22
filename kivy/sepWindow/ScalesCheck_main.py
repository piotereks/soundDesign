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


    # def on_touch_down(self,touch): 
    #     print(f"--down----------------{self}, {touch}") 
    #     return super(MainScreen, self).on_touch_down(touch)

    # def on_touch_up(self,touch): 
    #     print(f"--up----------------{self}, {touch}")
    #     return super(MainScreen, self).on_touch_up(touch)
    pass

class ScalesSelectScreen(Screen):


    # self.grid_rows=rows
    # self.grid_cols=cols
    # self.grid_len=rows*cols

    btn = ObjectProperty()
    button_matrix = ListProperty()
    # grid_rows=NumericProperty(13)
    # grid_cols=NumericProperty(4)
    # grid_len=NumericProperty(13*4)
    
    grid_rows=NumericProperty()
    grid_cols=NumericProperty()
    grid_len=NumericProperty()

    # pos_x = NumericProperty()
    grid_pos = ListProperty()



    but_id_offset = 0
    button_names = [ 'button_'+ str(i+1).rjust(3,'0')[-3:] for i in range(500)]
    nbr_of_scales = len(button_names)   

    def populate_button(self):
        # button_matix_len=self.grid_cols*self.grid_rows
        # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text='World 2'))
        # self.button_matrix=[]
        # for button_id in range(self.but_id_offset,self.but_id_offset+10):
        # for button_id in self.button_names:
        for button_id in self.button_names[self.but_id_offset:self.but_id_offset+self.grid_len]:
            btn = RadioButton(text=f'{button_id}')
            self.button_matrix.append(btn)
            # self.root.ids.scales_opt.ids.button_grid.add_widget(RadioButton(text=f'auto_{button_id}'))
            # self.root.ids.scales_opt.ids.button_grid.add_widget(btn)
            self.ids.button_grid.add_widget(btn)
            
        print('----------------')
    pass


    def rem_buttons(self):
        for button in self.button_matrix:
            # self.root.ids.scales_opt.remove_widget(button) 
            # self.root.ids.scales_opt.ids.button_grid.remove_widget(button)
            self.ids.button_grid.remove_widget(button)
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
        

     
    def on_touch_down(self,touch):
        print(f"down , {touch.__dict__=}, {touch.px=}, {touch.py=}, {touch.pos=}")
        # self.pos_x=touch.px
        self.grid_pos = touch.pos
        # return super(ScalesSelectScreen, self).on_touch_down(touch)
        # touch.grab(self)
        
    def on_touch_up(self,touch):
        if not self.grid_pos  or self.grid_pos == []:
            self.grid_pos = touch.pos
            return True
        print(f"up, {touch.__dict__=}, {touch.px=}, {touch.py=}, {touch.pos=}")
        # if self.pos_x-touch.px > 50:
        # print(f"{self.grid_pos=}, {self.grid_pos(0)=}, {touch.px=}")
        print(f"{self.grid_pos=}")
        print(f"{self.grid_pos[0]=}")
        # print(f"{self.grid_pos(0)=}")
        
        # if self.grid_pos[0]-touch.px > 50:
        print(f"{self.grid_pos[0]=},{touch.px=}, {self.grid_pos[0]-touch.px=}, {touch.dx=}")
        if self.grid_pos[0]-touch.x > 50:
            print('next')
            self.scale_page('next')
        # elif self.pos_x-touch.px <-50:
        if self.grid_pos[0]-touch.x <-50:
            print('prev')
            self.scale_page('prev')
            # return super(ScalesSelectScreen, self).on_touch_down(touch)
        # if self.pos == touch.pos:
        if pow(self.grid_pos[0]-touch.x,2)+pow(self.grid_pos[1]-touch.y,2) <=100:
            print('>>>>>>>equal<<<<<<<')
            self.grid_pos = touch.pos
            return super(ScalesSelectScreen, self).on_touch_down(touch)
        # touch.grab(self)
        self.grid_pos = touch.pos




        
        
class RadioButton(ToggleButtonBehavior, BoxLayout):
    text = StringProperty('')
    pass


class ScalesChkApp(App):
 
    selected_scale_button = StringProperty() 
    parm_rows=NumericProperty()
    parm_cols=NumericProperty()


    def on_selected_scale_button(self, instance, value):
        print(instance, value)
        print(self.selected_scale_button)    






#  self.manager.ids.another.ids.box.add_widget(Label(text="Button 1 pressed"))

if __name__ == '__main__':
    # ScalesSelectScreen(12,3)
    ScalesChkApp(parm_rows=7,parm_cols=3).run()