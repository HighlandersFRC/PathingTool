from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from data_assets.point import Point

from .angle_selector import AngleDial

class VelocityEditor(BoxLayout):
    def __init__(self, update_func, average_func, **kwargs):
        super().__init__(**kwargs)
        #selected key point
        self.selected_point = None

        #update callback
        self.update_func = update_func
        self.average_func = average_func

        #create and add widgets
        self.theta_dial = AngleDial(self.set_v_theta)
        self.v_theta_input = TextInput(hint_text = "VTheta (degr)", input_filter = "float", multiline = False, on_text_validate = self.update_v_theta)
        self.v_theta_button = Button(text = "Set VTheta", on_press = self.update_v_theta)
        self.v_mag_input = TextInput(hint_text = "VMagnitude (m)", input_filter = "float", multiline = False, on_text_validate = self.update_v_mag)
        self.v_mag_button = Button(text = "Set VMag", on_press = self.update_v_mag)
        self.average_button = Button(text = "Lin Cat.", on_press = self.average, background_color = (0.5, 0, 0, 1))
        self.add_widget(self.theta_dial)
        self.add_widget(self.v_theta_input)
        self.add_widget(self.v_theta_button)
        self.add_widget(self.v_mag_input)
        self.add_widget(self.v_mag_button)
        self.add_widget(self.average_button)

    #average point velocities
    def average(self, event):
        if self.selected_point == None:
            return
        self.average_func(self.selected_point.index)

    #set the velocity theta component
    def set_v_theta(self, theta: float):
        if self.selected_point == None:
            return
        self.selected_point.velocity_theta = theta
        self.v_theta_input.text = str(round(self.selected_point.get_vel_theta_degrees(), 2))  

    #update theta component
    def update_v_theta(self, event):
        if self.selected_point == None or self.v_theta_input.text == "":
            return
        self.selected_point.set_vel_theta_degrees(float(self.v_theta_input.text))
        self.update_func(self.selected_point)

    #update magnitude component
    def update_v_mag(self, event):
        if self.selected_point == None or self.v_mag_input.text == "":
            return
        self.selected_point.velocity_magnitude = float(self.v_mag_input.text)
        self.update_func(self.selected_point)

    #update selected point
    def update(self, point: Point):
        self.selected_point = point
        if self.selected_point == None:
            self.v_theta_input.text = ""
            self.v_mag_input.text = ""
            return
        self.v_theta_input.text = str(round(self.selected_point.get_vel_theta_degrees(), 2))
        self.v_mag_input.text = str(round(self.selected_point.velocity_magnitude, 2))