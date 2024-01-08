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
        self.cancel_button = Button(text = "Back", on_press = self.dismiss)
        self.add_command_button = Button(text = "Add Command", on_press = self.add_command)
        self.buttons_layout.add_widget(self.cancel_button)
        self.buttons_layout.add_widget(self.add_command_button)

    def add_command(self, event):
        self.commands.append(Command(len(self.commands), self.delete_command, self.key_points))
        self.update_func([c.get_command() for c in self.commands])

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

class Command(BoxLayout):
    def __init__(self, index: int, delete_func, key_points: list[Point], **kwargs):
        super().__init__(orientation = "horizontal", spacing = 0, **kwargs)
        self.index = index
        self.type = "angle_arm"
        self.args = [180]
        self.trigger_type = "time"
        self.trigger = 0

        self.types = ["angle_arm", "extend_arm", "intake", "placement"]
        self.triggers = ["time", "position"]

        self.key_points = key_points

        self.delete_func = delete_func

        self.type_menu = BoxLayout(orientation = "vertical", size_hint = (1, 1))
        self.trigger_type_menu = BoxLayout(orientation = "vertical", size_hint = (0.5, 1))
        self.trigger_menu = BoxLayout(orientation = "vertical", size_hint = (1, 1))
        self.extra_menu = BoxLayout(orientation = "vertical", size_hint = (0.5, 1))
        self.add_widget(self.type_menu)
        self.add_widget(self.trigger_type_menu)
        self.add_widget(self.trigger_menu)
        self.add_widget(self.extra_menu)

        self.angle_layout = BoxLayout(orientation = "horizontal")
        self.extend_layout = BoxLayout(orientation = "horizontal")
        self.intake_button = ToggleButton(text = "Intake", on_press = partial(self.select_type, 2), color = (1, 0.73, 0, 1))
        self.placement_button = ToggleButton(text = "Placement", on_press = partial(self.select_type, 3), color = (1, 0, 0, 1))
        self.type_menu.add_widget(self.angle_layout)
        self.type_menu.add_widget(self.extend_layout)
        self.type_menu.add_widget(self.intake_button)
        self.type_menu.add_widget(self.placement_button)
        
        self.angle_button = ToggleButton(text = "Angle\nArm", on_press = partial(self.select_type, 0), state = "down", color = (0, 0, 1, 1))
        self.angle_input = TextInput(hint_text = "Angle", input_filter = "float", multiline = False, on_text_validate = self.set_angle_arg)
        self.angle_layout.add_widget(self.angle_button)
        self.angle_layout.add_widget(self.angle_input)

        self.extend_button = ToggleButton(text = "Extend\nArm", on_press = partial(self.select_type, 1), color = (0, 1, 0, 1))
        self.extend_input = TextInput(hint_text = "Ext. Length", input_filter = "float", multiline = False, on_text_validate = self.set_extend_arg)
        self.extend_layout.add_widget(self.extend_button)
        self.extend_layout.add_widget(self.extend_input)

        self.time_button = ToggleButton(text = "Time\nTrigger", on_press = partial(self.select_trigger_type, 0), state = "down")
        self.position_button = ToggleButton(text = "Position\nTrigger", on_press = partial(self.select_trigger_type, 1))
        self.trigger_type_menu.add_widget(self.time_button)
        self.trigger_type_menu.add_widget(self.position_button)

        self.time_trigger = BoxLayout(orientation = "horizontal")
        self.position_trigger = BoxLayout(orientation = "horizontal")
        self.index_trigger = BoxLayout(orientation = "horizontal")
        self.trigger_menu.add_widget(self.time_trigger)
        self.trigger_menu.add_widget(self.index_trigger)

        self.time_trigger_input = TextInput(hint_text = "Time", input_filter = "float", multiline = False, on_text_validate = partial(self.select_trigger_type, 0))
        self.time_trigger_label = Label(text = "[b]Time[/b]", markup = True, outline_color = (1, 0, 0, 1))
        self.time_trigger.add_widget(self.time_trigger_label)
        self.time_trigger.add_widget(self.time_trigger_input)

        self.position_trigger_x_input = TextInput(hint_text = "X", input_filter = "float", multiline = False, on_text_validate = partial(self.select_trigger_type, 1))
        self.position_trigger_y_input = TextInput(hint_text = "Y", input_filter = "float", multiline = False, on_text_validate = partial(self.select_trigger_type, 1))
        self.position_trigger_label = Label(text = "[b]Position[/b]", markup = True)
        self.position_trigger.add_widget(self.position_trigger_label)
        self.position_trigger.add_widget(self.position_trigger_x_input)
        self.position_trigger.add_widget(self.position_trigger_y_input)

        self.index_trigger_input = TextInput(hint_text = "Index", input_filter = "int", multiline = False)
        self.index_trigger_button = ToggleButton(text = "Use\nPoint\nIndex", on_press = self.update_index_selection, on_release = self.update_index_selection)
        self.index_trigger.add_widget(self.index_trigger_button)
        self.index_trigger.add_widget(self.index_trigger_input)

        self.delete_button = Button(text = "Delete", on_press = self.delete, background_color = (1, 0, 0, 1))
        self.extra_menu.add_widget(self.delete_button)

    def select_type(self, type_int: int, event):
        type = self.types[type_int]
        self.deselect_all_types()
        if type == "angle_arm":
            self.angle_button.state = "down"
            self.type = "angle_arm"
            self.set_angle_arg(None)
        elif type == "extend_arm":
            self.extend_button.state = "down"
            self.type = "extend_arm"
            self.set_extend_arg(None)
        elif type == "intake":
            self.intake_button.state = "down"
            self.type = "intake"
            self.args = [1]
        elif type == "placement":
            self.placement_button.state = "down"
            self.type = "placement"
            self.args = [1]
        

    def deselect_all_types(self):
        self.angle_button.state = "normal"
        self.extend_button.state = "normal"
        self.intake_button.state = "normal"
        self.placement_button.state = "normal"

    def select_trigger_type(self, trigger_int: int, event):
        trigger_type = self.triggers[trigger_int]
        self.deselect_all_triggers()
        self.trigger_menu.clear_widgets()
        if trigger_type == "time":
            self.time_button.state = "down"
            self.trigger_type = "time"
            self.trigger_menu.add_widget(self.time_trigger)
            self.set_trigger(None)
        elif trigger_type == "position":
            self.position_button.state = "down"
            self.trigger_type = "position"
            self.trigger_menu.add_widget(self.position_trigger)
            self.set_trigger(None)
        self.trigger_menu.add_widget(self.index_trigger)

    def deselect_all_triggers(self):
        self.time_button.state = "normal"
        self.position_button.state = "normal"

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
            self.position_trigger_x_input.text = str(round(self.key_points[index].x, 2))
            self.position_trigger_y_input.text = str(round(self.key_points[index].y, 2))
        self.set_trigger(None)

    def set_trigger(self, event):
        if self.trigger_type == "time":
            if self.time_trigger_input.text != "" and self.time_trigger_input.text != ".":
                self.trigger = float(self.time_trigger_input.text)
        elif self.trigger_type == "position":
            if self.position_trigger_x_input.text != "" and self.position_trigger_x_input.text != "." and self.position_trigger_y_input.text != "" and self.position_trigger_y_input.text != ".":
                x = float(self.position_trigger_x_input.text)
                y = float(self.position_trigger_y_input.text)
                self.trigger = [x, y]

    def set_angle_arg(self, event):
        if self.type == "extend_arm" or self.angle_input.text == "" or self.angle_input.text == ".":
            return
        self.args = [float(self.angle_input.text)]

    def set_extend_arg(self, event):
        if self.type == "angle_arm" or self.extend_input.text == "" or self.extend_input.text == ".":
            return
        self.args = [float(self.extend_input.text)]

    def delete(self, event):
        self.delete_func(self.index, event)

    def update_inputs(self):
        self.deselect_all_types()
        self.deselect_all_triggers()
        if self.type == "angle_arm":
            self.angle_button.state = "down"
            self.angle_input.text = str(self.args[0])
        elif self.type == "extend_arm":
            self.extend_button.state = "down"
            self.extend_input.text = str(self.args[0])
        elif self.type == "intake":
            self.intake_button.state = "down"
        elif self.type == "placement":
            self.placement_button.state = "down"
        if self.trigger_type == "time":
            self.time_button.state = "down"
            self.time_trigger_input.text = str(self.trigger)
            self.select_trigger_type(0, None)
        elif self.trigger_type == "position":
            self.position_button.state = "down"
            self.position_trigger_x_input.text = str(self.trigger[0])
            self.position_trigger_y_input.text = str(self.trigger[1])
            self.select_trigger_type(1, None)

    def get_command(self):
        return {
            "trigger_type": self.trigger_type,
            "trigger": self.trigger,
            "command": {
                "type": self.type,
                "args": self.args
            }
        }

    def set_command(self, cmd: dict):
        self.trigger_type = cmd["trigger_type"]
        self.trigger = cmd["trigger"]
        self.type = cmd["command"]["type"]
        self.args = cmd["command"]["args"]
        self.set_angle_arg(None)
        self.set_extend_arg(None)
        self.update_index_selection(None)
        self.update_inputs()