from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from data_assets.point import Point

class EditValue(BoxLayout):
    def __init__(self, name: str, field: str, update_func, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #selected key point
        self.selected_point = None

        #update callback
        self.update_func = update_func
        #displayed name
        self.name = name
        #field accessed from selected point
        self.field = field

        #create and add sub-widgets
        self.value_input = TextInput(hint_text = f"{self.name} Value", input_filter = "float", multiline = False, on_text_validate = self.submit)
        self.submit_button = Button(text = f"Set {self.name}", on_press = self.submit)
        self.add_widget(self.value_input)
        self.add_widget(self.submit_button)

        if field == "delta_time":
            self.time_to_point_label = Label(text = "[b]Point Time[/b]", markup = True)
            self.add_widget(self.time_to_point_label)

    #submit button callback
    def submit(self, event):
        #if no point is selected do nothing
        if self.selected_point == None:
            return
        #convert input text to float
        value = float(self.value_input.text)
        #if input is empty do nothing
        if value == "":
            return
        #update selected point and call callback
        self.set_value(value)
        self.update_func(self.selected_point)

    #update the selected point and text field
    def update(self, point: Point):
        self.selected_point = point
        self.value_input.text = str(round(self.get_value(), 2))
        if self.field == "delta_time" and point != None:
            self.time_to_point_label.text = f"[b]Point Time: [color=#00ff00]{point.time}[/color][/b]"

    #get value from point field
    def get_value(self):
        if self.selected_point == None:
            return 0
        if self.field == "x":
            return self.selected_point.x
        if self.field == "y":
            return self.selected_point.y
        if self.field == "angle":
            return self.selected_point.get_angle_degrees()
        if self.field == "delta_time":
            return self.selected_point.delta_time

    #set value of point field
    def set_value(self, value: float):
        if self.selected_point == None:
            return
        if self.field == "x":
            self.selected_point.x = value
        if self.field == "y":
            self.selected_point.y = value
        if self.field == "angle":
            self.selected_point.set_angle_degrees(value)
        if self.field == "delta_time":
            self.selected_point.delta_time = value
           