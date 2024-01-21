from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ExtraControls(BoxLayout):
    def __init__(self, cat_func, visualize_func, command_func, **kwargs):
        super().__init__(**kwargs)
        #callbacks
        self.cat_func = cat_func
        self.visualize_func = visualize_func
        self.command_func = command_func
        
        #create and add widgets
        self.catmull_rom_button = Button(text = "Cat. ALL", on_press = self.cat_all, background_color = (0.5, 0, 0, 1))
        self.visualize_button = Button(text = "Visualizer", on_press = self.visualize)
        self.command_editor_button = Button(text = "Commands", on_press = self.edit_commands, background_color = (0.8, 0.8, 0, 1))
        self.add_widget(self.catmull_rom_button)
        self.add_widget(self.visualize_button)
        self.add_widget(self.command_editor_button)

    #catmull-rom all button callback
    def cat_all(self, event):
        self.cat_func()

    def visualize(self, event):
        self.visualize_func()

    def edit_commands(self, event):
        self.command_func()
