from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from functools import partial
from data_assets.point import Point

class CommandEditor(Popup):
    def __init__(self, update_func, **kwargs):
        super().__init__(title = "Command Editor", **kwargs)

        #update callback
        self.update_func = update_func

        #list of command objects
        self.commands = []

        #selected key point
        self.selected_point = None

        #list of key path points
        self.key_points = []

        #overall layout
        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        #sub layouts
        self.commands_layout = GridLayout(cols = 3, spacing = 4)
        self.buttons_layout = BoxLayout(orientation = "horizontal", size_hint = (1, 0.1))
        self.layout.add_widget(self.commands_layout)
        self.layout.add_widget(self.buttons_layout)

        #buttons for button layout
        self.cancel_button = Button(text = "Back", on_press = self.back_callback)
        self.add_command_button = Button(text = "Add Command", on_press = self.add_command)
        self.buttons_layout.add_widget(self.cancel_button)
        self.buttons_layout.add_widget(self.add_command_button)

    def add_command(self, event):
        self.commands.append(Command(len(self.commands), self.delete_command, self.key_points))
        self.update_func([c.get_command() for c in self.commands])
        self.update([c.get_command() for c in self.commands])

    def update(self, commands: list[dict]):
        self.commands = []
        for c in commands:
            self.commands.append(Command(len(self.commands), self.delete_command, self.key_points))
            self.commands[-1].set_command(c)
        self.index_commands()
        self.commands_layout.clear_widgets()
        for c in self.commands:
            self.commands_layout.add_widget(c)

    def update_key_points(self, key_points: list[Point]):
        self.key_points = key_points
        for c in self.commands:
            c.key_points = key_points

    def get_commands(self):
        return [c.get_command() for c in self.commands]

    def index_commands(self):
        for i in range(len(self.commands)):
            self.commands[i].index = i

    def delete_command(self, index: int, event):
        self.commands.pop(index)
        self.update_func([c.get_command() for c in self.commands])
        self.update([c.get_command() for c in self.commands])

    def back_callback(self, event):
        self.update_func([c.get_command() for c in self.commands])
        self.dismiss()

class Command(BoxLayout):
    def __init__(self, index: int, delete_func, key_points: list[Point], **kwargs):
        super().__init__(orientation = "horizontal", spacing = 0, **kwargs)
        self.index = index
        self.type = "shoot"
        self.halting = False
        self.args = [1]
        self.trigger_type = "time"
        self.trigger = 0

        self.types = ["shoot", "intake_down", "intake_up", "pause"]

        self.key_points = key_points

        self.delete_func = delete_func

        self.type_menu = BoxLayout(orientation = "vertical", size_hint = (1, 1))
        self.trigger_menu = BoxLayout(orientation = "vertical", size_hint = (1, 1))
        self.extra_menu = BoxLayout(orientation = "vertical", size_hint = (0.5, 1))
        

        self.shoot_layout = BoxLayout(orientation = "horizontal")
        self.intake_down_layout = BoxLayout(orientation = "horizontal")
        self.intake_up_layout = BoxLayout(orientation = "horizontal")
        self.pause_layout = BoxLayout(orientation = "horizontal")
        self.type_menu.add_widget(self.shoot_layout)
        self.type_menu.add_widget(self.intake_down_layout)
        self.type_menu.add_widget(self.intake_up_layout)
        self.type_menu.add_widget(self.pause_layout)
        
        self.shoot_button = ToggleButton(text = "Shoot", on_press = partial(self.select_type, 0), state = "down", color = (0, 0, 1, 1))
        self.shoot_layout.add_widget(self.shoot_button)

        self.intake_down_button = ToggleButton(text = "Intake\nDown", on_press = partial(self.select_type, 1), color = (1, 0.5, 0.5, 1))
        self.intake_down_layout.add_widget(self.intake_down_button)

        self.intake_up_button = ToggleButton(text = "Intake\nUp", on_press = partial(self.select_type, 2), color = (0.5, 1, 0, 1))
        self.intake_up_layout.add_widget(self.intake_up_button)

        self.pause_button = ToggleButton(text = "Pause", on_press = partial(self.select_type, 3), color = (1, 0, 0, 1))
        self.pause_input = TextInput(hint_text = "Pause\nDuration", input_filter = "float", multiline = False, on_text_validate = self.set_pause_duration)
        self.pause_layout.add_widget(self.pause_button)
        self.pause_layout.add_widget(self.pause_input)

        self.time_trigger = BoxLayout(orientation = "horizontal")
        self.index_trigger = BoxLayout(orientation = "horizontal")
        self.halting_button = ToggleButton(text = "Path Halting", on_press = self.set_halting, background_color = (1, 0.75, 0, 1))
        self.trigger_menu.add_widget(self.time_trigger)
        self.trigger_menu.add_widget(self.index_trigger)
        self.trigger_menu.add_widget(self.halting_button)

        self.time_trigger_input = TextInput(hint_text = "Time", input_filter = "float", multiline = False, on_text_validate = partial(self.set_trigger, 0))
        self.time_trigger_label = Label(text = "[b]Time[/b]", markup = True, outline_color = (1, 0, 0, 1))
        self.time_trigger.add_widget(self.time_trigger_label)
        self.time_trigger.add_widget(self.time_trigger_input)

        self.index_trigger_input = TextInput(hint_text = "Index", input_filter = "int", multiline = False)
        self.index_trigger_button = ToggleButton(text = "Use\nPoint\nIndex", on_press = self.update_index_selection, on_release = self.update_index_selection)
        self.index_trigger.add_widget(self.index_trigger_button)
        self.index_trigger.add_widget(self.index_trigger_input)

        self.delete_button = Button(text = "Delete", on_press = self.delete, background_color = (1, 0, 0, 1))
        self.extra_menu.add_widget(self.delete_button)

        self.add_widget(self.type_menu)
        self.add_widget(self.trigger_menu)
        self.add_widget(self.extra_menu)

    def select_type(self, type_int: int, event):
        type = self.types[type_int]
        self.deselect_all_types()
        if type == "shoot":
            self.shoot_button.state = "down"
            self.type = "shoot"
            self.args = [1]
        elif type == "intake_down":
            self.intake_down_button.state = "down"
            self.type = "intake_down"
            self.args = [1]
        elif type == "intake_up":
            self.intake_up_button.state = "down"
            self.type = "intake_up"
            self.args = [1]
        elif type == "pause":
            self.pause_button.state = "down"
            self.type = "pause"
            self.args = [1]

    def deselect_all_types(self):
        self.shoot_button.state = "normal"
        self.intake_down_button.state = "normal"
        self.intake_up_button.state = "normal"
        self.pause_button.state = "normal"

    def set_pause_duration(self, event):
        if self.type != "pause" or self.pause_input.text == "" or self.pause_input.text == ".":
            return
        self.args = [float(self.pause_input.text)]

    def set_halting(self, event):
        if self.halting_button.state == "normal":
            self.halting = False
        elif self.halting_button.state == "down":
            self.halting = True

    def update_index_selection(self, event):
        if self.index_trigger_input.text == "":
            self.index_trigger_button.state = "normal"
            return
        index = int(self.index_trigger_input.text)
        if len(self.key_points) == 0 or index >= len(self.key_points):
            self.index_trigger_button.state = "normal"
            return
        if self.index_trigger_button.state == "down":
            self.time_trigger_input.text = str(self.key_points[index].time)
        self.set_trigger(None)

    def set_trigger(self, event):
        if self.trigger_type == "time":
            if self.time_trigger_input.text != "" and self.time_trigger_input.text != ".":
                self.trigger = float(self.time_trigger_input.text)

    def delete(self, event):
        self.delete_func(self.index, event)

    def update_inputs(self):
        self.deselect_all_types()
        if self.type == "shoot":
            self.shoot_button.state = "down"
        elif self.type == "intake_down":
            self.intake_down_button.state = "down"
        elif self.type == "intake_up":
            self.intake_up_button.state = "down"
        elif self.type == "pause":
            self.pause_button.state = "down"
            self.pause_input.text = str(self.args[0])
        if self.trigger_type == "time":
            self.time_trigger_input.text = str(self.trigger)
            self.set_trigger(None)
        if self.halting:
            self.halting_button.state = "down"

    def get_command(self):
        return {
            "trigger_type": self.trigger_type,
            "trigger": self.trigger,
            "halting": self.halting,
            "command": {
                "type": self.type,
                "args": self.args
            }
        }

    def set_command(self, cmd: dict):
        self.trigger_type = cmd["trigger_type"]
        self.trigger = cmd["trigger"]
        self.halting = cmd["halting"]
        self.type = cmd["command"]["type"]
        self.args = cmd["command"]["args"]
        self.update_index_selection(None)
        self.update_inputs()