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
    scale_set_name_txt = StringProperty()
    selected_root_note = StringProperty()
    func_init_text = StringProperty()
    func_values = ListProperty()

 
    check_notes_lbl_text = StringProperty()
    queue_content_lbl_text = StringProperty()
    curr_notes_pair_lbl_text = StringProperty()
    fullq_content_lbl_text = StringProperty()
    prev_key = None    
    
    
    def build(self):
        return TrackerWidget()

if __name__ == "__main__":
    TrackerApp().run()