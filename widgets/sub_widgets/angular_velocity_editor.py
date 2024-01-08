from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class AngularVelocityEditor(BoxLayout):
    def __init__(self, update_func, average_func, **kwargs):
        super().__init__(**kwargs)
        #selected key point
        self.selected_point = None

        #callbacks
        self.update_func = update_func
        self.average_func = average_func

        #create and add widgets
        self.number_input = TextInput(hint_text = "VAng", input_filter = "float", multiline = False, on_text_validate = self.set_anguler_velocity)
        self.set_button = Button(text = "Set VAng", on_press = self.set_anguler_velocity)
        self.average_button = Button(text = "Ang Cat.", on_press = self.average, background_color = (0.5, 0, 0, 1))
        self.add_widget(self.number_input)
        self.add_widget(self.set_button)
        self.add_widget(self.average_button)

    #setter button callback
    def set_anguler_velocity(self, event):
        if self.selected_point == None or self.number_input.text == "" or self.number_input.text == ".":
            return
        self.selected_point.set_angular_velocity_degrees(float(self.number_input.text))
        self.update_func(self.selected_point)

    #average button callback
    def average(self, event):
        if self.selected_point == None:
            return
        self.average_func(self.selected_point.index)

    #update selected point
    def update(self, point):
        self.selected_point = point
        if self.selected_point == None:
            self.number_input.text = ""
            return
        self.number_input.text = str(round(self.selected_point.get_angular_velocity_degrees(), 2))