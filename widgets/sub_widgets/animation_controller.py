from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class AnimationController(BoxLayout):
    def __init__(self, run_func, recording_func,**kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #selected key point
        self.selected_point = None

        #run animation callback
        self.run_func = run_func
        self.recording_func = recording_func

        #create and add widgets
        self.run_full_button = Button(text = "Full", on_press = self.run_full)
        self.run_both_button = Button(text = "Run Both", on_press = self.run_both)
        self.run_from_point_button = Button(text = "From Point", on_press = self.run_from_point)
        self.run_recording_button = Button(text = "Recording", on_press = self.run_recording)
        self.add_widget(self.run_full_button)
        self.add_widget(self.run_both_button)
        self.add_widget(self.run_from_point_button)
        self.add_widget(self.run_recording_button)

    #run full animation
    def run_full(self, event):
        self.run_func(0.0)

    #run both ideal and recorded animation at same time
    def run_both(self, event):
        self.run_func(0.0)
        self.recording_func()

    #run animation starting at the selected point
    def run_from_point(self, event):
        if self.selected_point == None:
            return
        self.run_func(self.selected_point.time)

    def run_recording(self, event):
        self.recording_func()

    def update(self, selected_point):
        self.selected_point = selected_point