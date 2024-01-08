from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from widgets.sub_widgets.angle_selector import AngleSelector
from widgets.sub_widgets.edit_value import EditValue
from widgets.sub_widgets.nudge_value import NudgeValue
from widgets.sub_widgets.save_delete import SaveDelete
from widgets.sub_widgets.animation_controller import AnimationController
from widgets.sub_widgets.velocity_editor import VelocityEditor
from widgets.sub_widgets.angular_velocity_editor import AngularVelocityEditor
from widgets.sub_widgets.extra_controls import ExtraControls
from widgets.sub_widgets.info_bar import InfoBar
from data_assets.point import Point

from popups.save_load import SaveLoad
from popups.visualizer_menu import VisualizerMenu
from popups.command_editor import CommandEditor

class Editor(GridLayout):
    def __init__(self, update_func, delete_func, clear_func, animation_func, save_func, load_func, upload_func, upload_all_func, download_func, linear_average_func, angular_average_func, average_all_func, display_func, recording_func, clear_local_func, clear_rio_func, full_sample_func, update_commands_func, **kwargs):
        super().__init__(cols = 3, **kwargs)
        #selected key point
        self.selected_point = None
        #sampling rate
        self.sample_rate = 0.01
        #name of current path
        self.path_name = ""

        #callback functions in pathtool
        self.delete_func = delete_func
        self.clear_func = clear_func
        self.update_func = update_func
        self.display_func = display_func

        #editor sub-widgets
        self.edit_time = EditValue("Delta Time", "delta_time", self.update_selected_point)
        self.edit_x = EditValue("X", "x", self.update_selected_point)
        self.edit_y = EditValue("Y", "y", self.update_selected_point)
        self.angle_selector = AngleSelector(self.update_selected_point)
        self.nudge_x = NudgeValue("X", "x", (0, 0, 0.75, 1), (0, 0, 0.75, 1), self.update_selected_point)
        self.nudge_y = NudgeValue("Y", "y", (0.75, 0.75, 0.75, 1), (0.75, 0.75, 0.75, 1), self.update_selected_point)
        self.save_delete = SaveDelete(self.delete_point, self.clear_points, self.save_path, self.load_path, self.upload_path)
        self.velocity_editor = VelocityEditor(self.update_selected_point, linear_average_func)
        self.angular_velocity_editor = AngularVelocityEditor(self.update_selected_point, angular_average_func)
        self.animation_controller = AnimationController(animation_func, recording_func)
        self.extra_controls = ExtraControls(average_all_func, self.open_visualizer_menu, self.open_command_editor)
        self.info_bar = InfoBar()

        #add sub-widgets
        self.add_widget(self.edit_time)
        self.add_widget(self.edit_x)
        self.add_widget(self.nudge_x)
        self.add_widget(self.angle_selector)
        self.add_widget(self.edit_y)
        self.add_widget(self.nudge_y)
        self.add_widget(self.save_delete)
        self.add_widget(self.velocity_editor)
        self.add_widget(self.angular_velocity_editor)
        self.add_widget(self.animation_controller)
        self.add_widget(self.extra_controls)
        self.add_widget(self.info_bar)

        #popups
        self.save_load = SaveLoad(save_func, load_func, upload_func, upload_all_func, download_func)
        self.visualizer_menu = VisualizerMenu(display_func, full_sample_func, clear_local_func, clear_rio_func)
        self.command_editor = CommandEditor(update_commands_func)

    #delete selected point if a point is selected
    def delete_point(self):
        if self.selected_point == None:
            return
        #call callback in pathtool
        self.delete_func(self.selected_point.index)

    #clear key points
    def clear_points(self):
        self.clear_func()

    #open command editor popup
    def open_command_editor(self):
        self.command_editor.open()

    #open the visualizer menu
    def open_visualizer_menu(self):
        self.visualizer_menu.data_chooser.path = "./recorded_data"
        self.visualizer_menu.data_chooser.selection = []
        self.visualizer_menu.open()

    #save path to json
    def save_path(self):
        self.save_load.mode = "save"
        self.save_load.file_chooser.path = "./saves"
        self.save_load.file_chooser.selection = []
        self.save_load.text_box.text = self.path_name
        self.save_load.open()

    #load path from json
    def load_path(self):
        self.save_load.mode = "load"
        self.save_load.file_chooser.path = "./saves"
        self.save_load.open()

    #upload path to roborio
    def upload_path(self):
        print(self.path_name)
        self.save_load.mode = "save"
        self.save_load.file_chooser.path = "./saves"
        self.save_load.file_chooser.selection = []
        self.save_load.text_box.text = self.path_name
        self.save_load.open()

    #return the updated selected point
    def get_updated_point(self):
        return self.selected_point

    #update selected point and update sub-widgets
    def update_selected_point(self, point: Point):
        self.selected_point = point
        self.edit_time.update(self.selected_point)
        self.edit_x.update(self.selected_point)
        self.edit_y.update(self.selected_point)
        self.angle_selector.update(self.selected_point)
        self.nudge_x.update(self.selected_point)
        self.nudge_y.update(self.selected_point)
        self.velocity_editor.update(self.selected_point)
        self.angular_velocity_editor.update(self.selected_point)
        self.animation_controller.update(self.selected_point)
        self.update_func(update_editor = False)

    #update list of key points
    def update_command_key_points(self, key_points: list[Point]):
        self.command_editor.update_key_points(key_points)

    #update list of commands
    def update_commands(self, commands: list):
        self.command_editor.update(commands)

    #get list of commands
    def get_commands(self):
        return self.command_editor.get_commands()

    #update name of path
    def update_path_name(self, name: str):
        self.path_name = name

    #update displayed status message
    def update_status(self, text: str, color: tuple[float | int]):
        self.info_bar.update_status(text, color)

    def update_time(self, time: float):
        self.info_bar.update_time(time)
