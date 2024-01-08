from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import *

from data_assets.point import Point
import math

class AngleSelector(BoxLayout):
    def __init__(self, update_func, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #selected path point
        self.selected_point = None
        #update callback
        self.update_func = update_func

        #create and add widgets
        self.dial = AngleDial(self.update_angle)
        self.angle_input = TextInput(hint_text = "Angle (degrees)", input_filter = "float", multiline = False, on_text_validate = self.submit)
        self.submit_button = Button(text = "Set Angle", on_press = self.submit)
        self.add_widget(self.dial)
        self.add_widget(self.angle_input)
        self.add_widget(self.submit_button)

    #submit button callback
    def submit(self, event):
        #if a point is selected call update callback
        if self.selected_point == None:
            return
        self.selected_point.set_angle_degrees(float(self.angle_input.text))
        self.update_func(self.selected_point)

    #update selected point
    def update(self, point: Point):
        self.selected_point = point
        if self.selected_point == None:
            return
        self.angle_input.text = str(round(point.get_angle_degrees(), 2))

    #update selected point angle
    def update_angle(self, angle):
        if self.selected_point == None:
            return
        self.selected_point.angle = angle
        self.angle_input.text = str(round(self.selected_point.get_angle_degrees(), 2))

class AngleDial(Image):
    def __init__(self, update_func, **kwargs):
        super().__init__(source = "images/DialBackground.png", **kwargs)
        #update key callback
        self.update_func = update_func
        #white line on dial
        self.angle_line = Line()

    #click drag callback
    def on_touch_move(self, touch):
        if super().on_touch_move(touch):
            return True

        #if drag is on dial widget update angle and draw line
        if self.collide_point(touch.x, touch.y):
            angle = math.atan2(touch.y - self.center_y, touch.x - self.center_x)
            self.update_func(angle)
            self.canvas.remove(self.angle_line)
            self.angle_line = Line(width = 2, cap = "round", points = [self.center_x, self.center_y, min(self.size) / 2 * math.cos(angle) + self.center_x, min(self.size) / 2 * math.sin(angle) + self.center_y])
            self.canvas.add(self.angle_line)