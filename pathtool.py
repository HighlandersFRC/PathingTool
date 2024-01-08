from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

from widgets.path import Path
from widgets.points_menu import PointsMenu
from widgets.editor import Editor
from data_assets.point import Point
from tools import convert
from tools import file_manager
from popups.save_load import SaveLoad
from SplineGeneration.generateSplines import SplineGenerator
import math
import matplotlib.pyplot as plt

class PathTool(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #main widgets
        self.editor_viewer_layout = BoxLayout(orientation = "vertical")
        self.editor = Editor(self.update_widgets, self.delete_point, self.clear_points, self.run_animation, self.save_path, self.load_path, self.upload_path, self.upload_all_paths, self.download_all_paths, self.average_linear_velocity, self.average_angular_velocity, self.average_all, self.display_recording, self.run_recording, self.clear_local_recordings, self.clear_rio_recordings, self.get_sampled_points, self.update_commands, size_hint = (1, 0.25))
        self.path = Path(self.get_sampled_point, size_hint = (1, 1.5), allow_stretch = True, keep_ratio = False)
        self.points_menu = PointsMenu(self.update_path, size_hint = (0.1, 1), padding = [2, 2, 2, 2], spacing = 1)
        self.set_layout()

        self.spline_generator = SplineGenerator()

        #list of commands
        self.commands = []
        #list of key points
        self.key_points = []
        #currently selected point
        self.selected_point = None
        #how often path is sample in seconds
        self.sample_rate = 0.01
        #amount of time at the end to give PIDs to settle
        self.end_time_pad = 5 / 50
        #name of current path
        self.path_name = ""
        #ip address of the roborio
        self.rio_address = "10.44.99.2"
        # self.rio_address = "172.22.11.2"

        #physical limitations of the robot
        self.MAX_LINEAR_ACCEL = 6
        self.MAX_LINEAR_VEL = 4
        self.MAX_ANGULAR_ACCEL = 1.5 * 2 * math.pi
        self.MAX_ANGULAR_VEL = 1.5 * 2 * math.pi

    #add widgets to main layout
    def set_layout(self):
        self.editor_viewer_layout.add_widget(self.editor)
        self.editor_viewer_layout.add_widget(self.path)
        self.add_widget(self.editor_viewer_layout)
        self.add_widget(self.points_menu)

    #called on click events
    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True

        #Click on the field
        if self.path.collide_point(touch.x, touch.y):
            self.selected_point = self.path.get_selected_point(touch.x, touch.y)

            #if no point is selected add new point
            if self.selected_point == None:
                pos = convert.pixels_to_meters((touch.x, touch.y), self.path.size)
                if len(self.key_points) > 0:
                    self.selected_point = Point(len(self.key_points), 1.0, pos[0], pos[1], 0.0, 1.0, 0.0, 0.0)
                else:
                    self.selected_point = Point(len(self.key_points), 0.0, pos[0], pos[1], 0.0, 0.0, 0.0, 0.0)
                self.key_points.append(self.selected_point)
            #else update selected point
            else:
                self.editor.update_selected_point(self.selected_point)

        #Click on the editor
        if self.editor.collide_point(touch.x, touch.y):
            self.selected_point = self.editor.get_updated_point()

            #if no point is selected do nothing
            if self.selected_point == None:
                return True
            #else update selected point
            else:
                self.key_points[self.selected_point.index] = self.selected_point

        #update main widgets
        self.update_widgets()

    #update main widgets
    def update_widgets(self, update_editor = True, update_equations = True):
        #update indexes and times
        self.index_points()
        self.time_points()
        self.optimize_points()
        self.commands = self.editor.get_commands()
        #if multiple points update equations
        if len(self.key_points) > 1 and update_equations:
            self.spline_generator.generateSplineCurves([[p.time, p.x, p.y, p.angle, p.velocity_magnitude * math.cos(p.velocity_theta), p.velocity_magnitude * math.sin(p.velocity_theta), p.angular_velocity, 0.0, 0.0, 0.0] for p in self.key_points])
            self.path.update(self.key_points, self.get_sampled_points(colors = True, times = True), self.sample_rate, self.commands)
        else:
            self.path.update(self.key_points, [], self.sample_rate, self.commands)
        self.points_menu.update(self.key_points, self.selected_point)
        #update selected point in widgets
        if update_editor:
            self.editor.update_selected_point(self.selected_point)
            self.editor.update_path_name(self.path_name)
            self.editor.update_commands(self.commands)
            self.editor.update_command_key_points(self.key_points)
            if len(self.key_points) > 0:
                self.editor.update_time(self.key_points[-1].time)
            else:
                self.editor.update_time(0.0)
        self.path.update_selected_point(self.selected_point)

    #update key points and selected point
    def update_path(self, key_points: list[Point], selected_point: Point, update_equations = True):
        self.selected_point = selected_point
        self.key_points = key_points
        self.update_widgets(update_equations = update_equations)

    #update the command list
    def update_commands(self, commands: list):
        self.commands = commands
        self.update_widgets(update_equations = False)

    #display recorded path over the field image
    def display_recording(self, recording: list):
        self.path.set_recording(recording)

    #run recording animation
    def run_recording(self):
        self.path.set_recording_animation()

    #delete selected point
    def delete_point(self, index):
        #if removed point is the first point set new first point velocity to zero
        if index == 0 and len(self.key_points) > 1:
            self.key_points[1].velocity_magnitude = 0
            self.key_points[1].delta_time = 0
        #remove point
        self.key_points.pop(index)
        #if removed point is the selected point (which it should be) clear selected point
        if self.selected_point.index == index:
            self.selected_point = None
        #update main widgets
        self.update_widgets()

    #clear key points
    def clear_points(self):
        #clear key points, selected point, and update main widgets
        self.key_points = []
        self.selected_point = None
        self.update_widgets()

    #re-index points
    def index_points(self):
        for i in range(len(self.key_points)):
            self.key_points[i].index = i

    #update time values for each point
    def time_points(self):
        time = 0.0
        for p in self.key_points:
            time += p.delta_time
            p.time = time

    #optize the angles of the key points
    def optimize_points(self):
        for i in range(1, len(self.key_points)):
            p1 = self.key_points[i - 1]
            p2 = self.key_points[i]
            p2.angle %= 2 * math.pi
            if p2.angle - p1.angle > math.pi:
                p2.angle -= 2 * math.pi
            elif p2.angle - p1.angle < -math.pi:
                p2.angle += 2 * math.pi

    #apply catmull-rom on linear splines
    def average_linear_velocity(self, index: int, update_widgets = True):
        if self.key_points[index].index != 0 and self.key_points[index].index != len(self.key_points) - 1:
            p0 = self.key_points[self.key_points[index].index - 1]
            p2 = self.key_points[self.key_points[index].index + 1]
            dt = p2.time - p0.time
            v_theta = math.atan2(p2.y - p0.y, p2.x - p0.x)
            dist = convert.get_dist(p0.x, p0.y, p2.x, p2.y)
            v_mag = dist / dt
            self.key_points[index].velocity_magnitude = v_mag
            self.key_points[index].velocity_theta = v_theta
        else:
            self.key_points[index].velocity_magnitude = 0
            self.key_points[index].velocity_theta = 0
        if update_widgets:
            self.update_widgets()

    #apply catmull-rom  on angular spline
    def average_angular_velocity(self, index: int, update_widgets = True):
        if self.key_points[index].index != 0 and self.key_points[index].index != len(self.key_points) - 1:
            p0 = self.key_points[index - 1]
            p1 = self.key_points[index]
            p2 = self.key_points[index + 1]
            dt = p2.time - p0.time
            da = p2.angle - p0.angle
            if p2.angle - p0.angle > math.pi:
                da = math.pi - da
            elif p2.angle - p0.angle < -math.pi:
                da = math.pi + da
            sine1 = self.get_optimized_rotation_sine(p0.angle, self.key_points[index].angle)
            sine2 = self.get_optimized_rotation_sine(self.key_points[index].angle, p2.angle)
            if sine1 != sine2:
                self.key_points[index].angular_velocity = 0
            else:
                self.key_points[index].angular_velocity = da / dt
            if abs(p0.angle - p1.angle) < math.pi / 8:
                self.key_points[index].angular_velocity = 0
            elif abs(p1.angle - p2.angle) < math.pi / 8:
                self.key_points[index].angular_velocity = 0
        else:
            self.key_points[index].angular_velocity = 0
        if update_widgets:
            self.update_widgets()

    #apply linear and angular catmull-rom on all points
    def average_all(self):
        for p in self.key_points:
            self.average_linear_velocity(p.index, update_widgets = False)
            self.average_angular_velocity(p.index, update_widgets = False)
        self.update_widgets()

    #angular optimizer
    def get_optimized_rotation_sine(self, angle1, angle2):
        if angle1 >= angle2:
            op2 = ((math.pi * 2) - (angle1 - angle2))
            op1 = (angle1 - angle2)
        else:
            op1 = ((math.pi * 2) - (angle2 - angle1))
            op2 = (angle2 - angle1)
        if op1 <= op2:
            return -1
        else:
            return 1

    #get list of sampled points
    def get_sampled_points(self, times = False, colors = False):
        sampled_points = []
        t = 0
        if len(self.key_points) <= 1:
            return
        while t <= self.key_points[-1].time:
            point = self.spline_generator.sample_pos(self.key_points, t)
            if times or colors:
                point.insert(0, t)
            sampled_points.append(point)
            t += self.sample_rate
        if colors:
            sampled_points = self.add_color_indicators(sampled_points)
        last_point = [0, 0, 0, 0, (0, 0, 0)]
        last_point[0] = sampled_points[-1][0] + self.end_time_pad
        last_point[1] = sampled_points[-1][1]
        last_point[2] = sampled_points[-1][2]
        last_point[3] = sampled_points[-1][3]
        sampled_points.append(last_point)
        return sampled_points

    #get single sampled point by time
    def get_sampled_point(self, time: float, include_time = False):
        if len(self.key_points) <= 1:
            return [0, 0]
        if include_time:
            point = self.spline_generator.sample_pos(self.key_points, time)
            point.insert(0, time)
            return point
        else:
            return self.spline_generator.sample_pos(self.key_points, time)
    
    #add colors indicating when physical limitations are exceeded by the path
    def add_color_indicators(self, points: list[list]):
        lin_vel_list = []
        lin_accel_list = []
        raw_info = []
        for p in points:
            lin_vel = self.spline_generator.sample_lin_vel(self.key_points, p[0])
            lin_accel = self.spline_generator.sample_lin_accel(self.key_points, p[0])
            lin_vel_list.append(lin_vel)
            lin_accel_list.append(lin_accel)
            if abs(lin_vel) > self.MAX_LINEAR_VEL and abs(lin_accel) > self.MAX_LINEAR_ACCEL:
                p.append((1, 0, 1))
            elif abs(lin_vel) > self.MAX_LINEAR_VEL:
                p.append((1, 0, 0))
            elif abs(lin_accel) > self.MAX_LINEAR_ACCEL:
                p.append((0, 0, 1))
            else:
                p.append((0, 0, 0))
            # raw_info.append(self.spline_generator.sample_raw_linear_info(self.key_points, p[0]))
        # plt.plot([p[0] for p in points], lin_accel_list, color = (0, 1, 0, 1))
        # plt.plot([p[0] for p in points], lin_vel_list, color = (1, 0, 0, 1))
        # plt.plot([p[0] for p in points], [entry[0] for entry in raw_info], color = (1, 0, 0, 1))
        # plt.plot([p[0] for p in points], [entry[2] for entry in raw_info], color = (0.6, 0, 0, 1))
        # plt.plot([p[0] for p in points], [entry[4] for entry in raw_info], color = (0.3, 0, 0, 1))
        # plt.plot([p[0] for p in points], [entry[1] for entry in raw_info], color = (0, 1, 0, 1))
        # plt.plot([p[0] for p in points], [entry[3] for entry in raw_info], color = (0, 0.6, 0, 1))
        # plt.plot([p[0] for p in points], [entry[5] for entry in raw_info], color = (0, 0.3, 0, 1))
        # plt.show()
        return points

    #start path animation from a time
    def run_animation(self, start_time: float):
        self.update_widgets()
        if len(self.key_points) > 1:
            self.path.set_animation(start_time)

    #save path as json file
    def save_path(self, folder_path: str, file_name: str, sample_rate: float):
        print(f"saving {folder_path}\\{file_name}.json")
        self.sample_rate = sample_rate
        self.path_name = file_name
        sampled_points = self.get_sampled_points(times = True)
        self.commands = self.editor.get_commands()
        result = file_manager.save_path(self.key_points, self.commands, sampled_points, self.sample_rate, folder_path, file_name)
        self.update_widgets()
        #update status
        if result:
            self.editor.update_status("[b]Path Saved[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Save Failed[/b]", (1, 0.25, 0.25, 1))

    #open json save file
    def load_path(self, file_path: str):
        print(f"loading {file_path}")
        path_data = file_manager.load_path(file_path)
        self.key_points = path_data[0]
        self.sample_rate = path_data[1]
        self.path_name = path_data[2]
        # self.commands = path_data[3]
        self.selected_point = None
        self.update_widgets()
        #update status
        if self.path_name == "":
            self.editor.update_status("[b]Load Failed[/b]", (1, 0.25, 0.25, 1))
        else:
            self.editor.update_status("[b]Path Loaded[/b]", (0.25, 1, 0.25, 1))

    #upload the current path
    def upload_path(self, file_path: str, folder_path: str, file_name: str, sample_rate: float):
        self.save_path(folder_path, file_name, sample_rate)
        result = file_manager.upload(self.rio_address, file_path)
        if result:
            self.editor.update_status("[b]Path Uploaded[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Upload Failed[/b]", (1, 0.25, 0.25, 1))

    #upload all paths
    def upload_all_paths(self, folder_path: str, file_name: str, sample_rate: float):
        self.save_path(folder_path, file_name, sample_rate)
        result = file_manager.upload_all(self.rio_address)
        if result:
            self.editor.update_status("[b]Uploaded All Paths[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Upload All Failed[/b]", (1, 0.25, 0.25, 1))

    #download all paths
    def download_all_paths(self):
        result = file_manager.download_all(self.rio_address)
        if result:
            self.editor.update_status("[b]All Paths Downloaded[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Download All Failed[/b]", (1, 0.25, 0.25, 1))

    #clear all local csv recordings
    def clear_local_recordings(self):
        result = file_manager.clear_local_recordings()
        if result:
            self.editor.update_status("[b]Local Recordings Cleared[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Clear Local Rec. Failed[/b]", (1, 0.25, 0.25, 1))

    #clear all csv recordings on the roborio
    def clear_rio_recordings(self):
        result = file_manager.clear_rio_recordings(self.rio_address)
        if result:
            self.editor.update_status("[b]Rio Recordings Cleared[/b]", (0.25, 1, 0.25, 1))
        else:
            self.editor.update_status("[b]Clear Rio Rec. Failed[/b]", (1, 0.25, 0.25, 1))