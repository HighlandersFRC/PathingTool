from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from data_assets.point import Point

class NudgeValue(BoxLayout):
    def __init__(self, name: str, field: str, pos_color: tuple, neg_color: tuple, update_func, **kwargs):
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
        self.increment_button = Button(text = f"+{self.name}", on_press = self.increment, background_color = pos_color)
        self.decrement_button = Button(text = f"-{self.name}", on_press = self.decrement, background_color = neg_color)
        self.add_widget(self.decrement_button)
        self.add_widget(self.increment_button)

    #nudge towards positive
    def increment(self, event):
        #if no point is selected do nothing
        if self.selected_point == None:
            return
        #update selected point and call callback
        self.set_value(self.get_value() + 0.025)
        self.update_func(self.selected_point)

    #nudge towards negative
    def decrement(self, event):
        #if no point is selected do nothing
        if self.selected_point == None:
            return
        #update selected point and call callback
        self.set_value(self.get_value() - 0.025)
        self.update_func(self.selected_point)

    #update selected point
    def update(self, point: Point):
        self.selected_point = point

    #get value from point field
    def get_value(self):
        if self.selected_point == None:
            return 0
        if self.field == "x":
            return self.selected_point.x
        if self.field == "y":
            return self.selected_point.y

    #set value of point field
    def set_value(self, value: float):
        if self.selected_point == None:
            return
        if self.field == "x":
            self.selected_point.x = value
        if self.field == "y":
            self.selected_point.y = value