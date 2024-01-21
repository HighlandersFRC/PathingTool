from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import *
from tools import convert
from SplineGeneration import generateSplines
import math
import time

class Path(Image):
    def __init__(self, sample_func, **kwargs):
        super().__init__(source = "images/CrescendoField.png", **kwargs)
        self.key_points = []
        self.sampled_points = []
        self.selected_point = None

        #seconds
        self.sample_rate = 0.01

        #[t, x, y, theta]
        #in seconds, meters, meters, radians
        self.recorded_points = []

        #autonomous commands
        self.commands = []

        #robot dimensions in meters
        self.robot_length = 0.73025
        self.robot_width = 0.635
        self.robot_radius = convert.get_robot_radius(self.robot_width, self.robot_length)

        #image of field
        self.field_image = Rectangle(source = "images/CrescendoField.png", pos = self.pos)

        #main instructions/instruction groups
        self.non_selected_points_group = InstructionGroup()
        self.selected_points_group = InstructionGroup()
        self.angle_indicators_group = InstructionGroup()
        self.velocity_indicators_group = InstructionGroup()
        self.animation_group = InstructionGroup()
        self.recording_animation_group = InstructionGroup()
        self.recording_line = Line()
        self.path_line = Line()
        self.path_line_group = InstructionGroup()
        self.command_group = InstructionGroup()

        #animation time in seconds
        self.animation_time = -1
        self.recording_animation_time = -1
        self.sample_func = sample_func

        #infomation text
        self.info_label = Label(text = "[b]PX:[/b] null, [b]PY:[/b]\n[b]X:[/b] null, [b]Y:[/b] null\n[b]Dist:[/b] null", markup = True, font_size = 12, color = (0, 0, 0))
        self.info_rect = Rectangle()
        
    #draw points and path line
    def draw_path(self, dt: float):
        # start_time = time.time_ns() / 1000000
        #erase non-selected points, selected point, angle indicators
        self.non_selected_points_group.clear()
        self.selected_points_group.clear()
        self.angle_indicators_group.clear()
        self.velocity_indicators_group.clear()
        self.animation_group.clear()
        self.recording_animation_group.clear()
        self.path_line_group.clear()
        self.command_group.clear()
        self.canvas.clear()
        self.field_image.size = self.size
        self.canvas.add(Rectangle(pos = (0, 0), size = self.size))
        self.canvas.add(self.field_image)

        #if more that 1 point in path generate spline line and add it
        if len(self.key_points) > 1:
            pixel_list = []
            color = self.sampled_points[0][4]
            for i in range(len(self.sampled_points)):
                p = self.sampled_points[i]
                px = convert.meters_to_pixels_x(p[1], self.size)
                py = convert.meters_to_pixels_y(p[2], self.size)
                pixel_list.append(px)
                pixel_list.append(py)
                if p[4] != color or i == len(self.sampled_points) - 1:
                    self.path_line_group.add(Color(color[0], color[1], color[2]))
                    self.path_line_group.add(Line(points = pixel_list, width = 2, cap = "round", joint = "round"))
                    color = p[4]
                    pixel_list = [px, py]
            self.canvas.add(self.path_line_group)

        #draw non-selected points and angle indicators
        for p in self.key_points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)

            self.non_selected_points_group.add(Color(0.6, 0, 0.6))
            #non-selected points
            if self.selected_point == None:
                self.non_selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))
            elif self.selected_point.index != p.index:
                self.non_selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 5, pixel_pos[1] - 5), size = (10, 10)))

            #angle indicators
            #angle from 0 to first corner
            corner_1_theta = math.atan2((self.robot_width) / (self.robot_radius * 2), (self.robot_length) / (self.robot_radius * 2))
            #corner angles
            theta_1 = corner_1_theta + p.angle
            theta_2 = math.pi - corner_1_theta + p.angle
            theta_3 = math.pi + corner_1_theta + p.angle
            theta_4 = 2 * math.pi - corner_1_theta + p.angle
            #corner coordinates in pixels
            corner_1 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_1) + p.x, self.robot_radius * math.sin(theta_1) + p.y), self.size)
            corner_2 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_2) + p.x, self.robot_radius * math.sin(theta_2) + p.y), self.size)
            corner_3 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_3) + p.x, self.robot_radius * math.sin(theta_3) + p.y), self.size)
            corner_4 = convert.meters_to_pixels((self.robot_radius * math.cos(theta_4) + p.x, self.robot_radius * math.sin(theta_4) + p.y), self.size)
            self.angle_indicators_group.add(Line(width = 2, cap = "square", joint = "miter", close = True, points = [corner_1[0], corner_1[1], corner_2[0], corner_2[1], corner_3[0], corner_3[1], corner_4[0], corner_4[1]]))
            #robot direction indicator
            front = convert.meters_to_pixels(((self.robot_length / 2.0) * math.cos(p.angle) + p.x, (self.robot_length / 2.0) * math.sin(p.angle) + p.y), self.size)
            self.angle_indicators_group.add(Line(width = 2, cap = "square", joint = "miter", points = [pixel_pos[0], pixel_pos[1], front[0], front[1]]))

            #velocity indicators
            self.velocity_indicators_group.add(Color(0, 0.75, 0))
            linear_pos = convert.meters_to_pixels(p.get_vel_marker_pos(), self.size)
            linear_dist = convert.get_dist(pixel_pos[0], pixel_pos[1], linear_pos[0], linear_pos[1])
            self.velocity_indicators_group.add(Line(width = 2, cap = "square", points = [pixel_pos[0], pixel_pos[1], linear_pos[0], linear_pos[1]]))
            # if p.get_angular_velocity_degrees() != 0:
            #     if linear_dist > 20:
            #         self.velocity_indicators_group.add(Line(width = 2, circle = (pixel_pos[0], pixel_pos[1], linear_dist, -p.get_vel_theta_degrees() - p.get_angular_velocity_degrees() + 90, -p.get_vel_theta_degrees() + 90)))
            #     else:
            #         self.velocity_indicators_group.add(Line(width = 2, circle = (pixel_pos[0], pixel_pos[1], 20, -p.get_vel_theta_degrees() - p.get_angular_velocity_degrees() + 90, -p.get_vel_theta_degrees() + 90)))
            
        #animation
        if len(self.key_points) > 1:
            if self.animation_time <= self.key_points[-1].time and self.animation_time >= 0:
                anim_point = self.sample_func(self.animation_time)
                anim_angle = anim_point[2]
                anim_pixel_point = convert.meters_to_pixels((anim_point[0], anim_point[1]), self.size)
                anim_front = convert.meters_to_pixels(((self.robot_length / 2.0) * math.cos(anim_angle) + anim_point[0], (self.robot_length / 2.0) * math.sin(anim_angle) + anim_point[1]), self.size)
                self.animation_group.add(Color(0, 0.4, 0.8))
                self.animation_group.add(Line(width = 2, cap = "square", joint = "miter", points = [anim_pixel_point[0], anim_pixel_point[1], anim_front[0], anim_front[1]]))
                corner_1_theta = math.atan2((self.robot_width) / (self.robot_radius * 2), (self.robot_length) / (self.robot_radius * 2))
                anim_theta_1 = corner_1_theta + anim_angle
                anim_theta_2 = math.pi - corner_1_theta + anim_angle
                anim_theta_3 = math.pi + corner_1_theta + anim_angle
                anim_theta_4 = 2 * math.pi - corner_1_theta + anim_angle
                anim_corner_1 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_1) + anim_point[0], self.robot_radius * math.sin(anim_theta_1) + anim_point[1]), self.size)
                anim_corner_2 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_2) + anim_point[0], self.robot_radius * math.sin(anim_theta_2) + anim_point[1]), self.size)
                anim_corner_3 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_3) + anim_point[0], self.robot_radius * math.sin(anim_theta_3) + anim_point[1]), self.size)
                anim_corner_4 = convert.meters_to_pixels((self.robot_radius * math.cos(anim_theta_4) + anim_point[0], self.robot_radius * math.sin(anim_theta_4) + anim_point[1]), self.size)
                self.animation_group.add(Line(width = 2, cap = "square", joint = "miter", close = True, points = [anim_corner_1[0], anim_corner_1[1], anim_corner_2[0], anim_corner_2[1], anim_corner_3[0], anim_corner_3[1], anim_corner_4[0], anim_corner_4[1]]))
                self.animation_time += dt
            if self.animation_time > self.key_points[-1].time:
                self.animation_time = 1000
        self.canvas.add(self.velocity_indicators_group)
        self.canvas.add(self.non_selected_points_group)
        self.canvas.add(self.angle_indicators_group)
        self.canvas.add(self.animation_group)

        #recording animation
        if len(self.recorded_points) > 1:
            if self.recording_animation_time <= self.recorded_points[-1][0] and self.recording_animation_time >= 0:
                recorded_point = self.recorded_points[0]
                for i in range(len(self.recorded_points) - 1):
                    if self.recording_animation_time >= self.recorded_points[i][0] and self.recording_animation_time <= self.recorded_points[i + 1][0]:
                        recorded_point = self.recorded_points[i]
                        break
                recorded_angle = recorded_point[3]
                recorded_pixel_point = convert.meters_to_pixels((recorded_point[1], recorded_point[2]), self.size)
                recorded_front = convert.meters_to_pixels(((self.robot_length / 2.0) * math.cos(recorded_angle) + recorded_point[1], (self.robot_length / 2.0) * math.sin(recorded_angle) + recorded_point[2]), self.size)
                self.recording_animation_group.add(Color(0, 0.75, 0))
                self.recording_animation_group.add(Line(width = 2, cap = "square", joint = "miter", points = [recorded_pixel_point[0], recorded_pixel_point[1], recorded_front[0], recorded_front[1]]))
                recorded_corner_1_theta = math.atan2(self.robot_width / (self.robot_radius * 2), self.robot_length / (self.robot_radius * 2))
                recorded_theta_1 = recorded_corner_1_theta + recorded_angle
                recorded_theta_2 = math.pi - recorded_corner_1_theta + recorded_angle
                recorded_theta_3 = math.pi + recorded_corner_1_theta + recorded_angle
                recorded_theta_4 = 2 * math.pi - recorded_corner_1_theta + recorded_angle
                recorded_corner_1 = convert.meters_to_pixels((self.robot_radius * math.cos(recorded_theta_1) + recorded_point[1], self.robot_radius * math.sin(recorded_theta_1) + recorded_point[2]), self.size)
                recorded_corner_2 = convert.meters_to_pixels((self.robot_radius * math.cos(recorded_theta_2) + recorded_point[1], self.robot_radius * math.sin(recorded_theta_2) + recorded_point[2]), self.size)
                recorded_corner_3 = convert.meters_to_pixels((self.robot_radius * math.cos(recorded_theta_3) + recorded_point[1], self.robot_radius * math.sin(recorded_theta_3) + recorded_point[2]), self.size)
                recorded_corner_4 = convert.meters_to_pixels((self.robot_radius * math.cos(recorded_theta_4) + recorded_point[1], self.robot_radius * math.sin(recorded_theta_4) + recorded_point[2]), self.size)
                self.recording_animation_group.add(Line(width = 2, cap = "square", joint = "miter", close = True, points = [recorded_corner_1[0], recorded_corner_1[1], recorded_corner_2[0], recorded_corner_2[1], recorded_corner_3[0], recorded_corner_3[1], recorded_corner_4[0], recorded_corner_4[1]]))
                self.recording_animation_time += dt
            if self.recording_animation_time > self.recorded_points[-1][0]:
                self.recording_animation_time = 1000
            self.canvas.add(self.recording_animation_group)

        #draw selected point
        if self.selected_point != None:
            pixel_pos = convert.meters_to_pixels((self.selected_point.x, self.selected_point.y), self.size)
            self.canvas.add(Color(1, 0, 1))
            self.selected_points_group.add(Ellipse(pos = (pixel_pos[0] - 7, pixel_pos[1] - 7), size = (14, 14)))
        self.canvas.add(self.selected_points_group)

        if len(self.recorded_points) > 0:
            xy_list = [None for i in range(len(self.recorded_points) * 2)]
            xy_list[::2] = [convert.meters_to_pixels_x(p[1], self.size) for p in self.recorded_points]
            xy_list[1::2] = [convert.meters_to_pixels_y(p[2], self.size) for p in self.recorded_points]
            self.recording_line = Line(width = 2, cap = "round", joint = "round", points = xy_list)
            self.canvas.add(Color(0, 0.5, 0))
            self.canvas.add(self.recording_line)

        #draw command indicators
        for c in self.commands:
            color = (0, 0, 0, 1)
            if c["command"]["type"] == "shoot":
                color = (0, 0, 0.9, 1)
            elif c["command"]["type"] == "intake_down":
                color = (0, 0.9, 0, 1)
            elif c["command"]["type"] == "intake_up":
                color = (0.9, 0, 0, 1)
            px = 0
            py = 0
            if c["trigger_type"] == "time":
                p = self.sample_func(c["trigger"])
                px, py = convert.meters_to_pixels(p, self.size)
            elif c["trigger_type"] == "position":
                px = convert.meters_to_pixels_x(c["trigger"][0], self.size)
                py = convert.meters_to_pixels_y(c["trigger"][1], self.size)
            self.command_group.add(Color(color[0], color[1], color[2]))
            self.command_group.add(Line(points = [px + 4, py, px, py - 4, px - 4, py, px, py + 4], cap = "square", joint = "miter", width = 3, close = True))
        self.canvas.add(self.command_group)

        #update infomational text
        self.update_info()
        # print(f"Draw: {time.time_ns() / 1000000 - start_time}")

    def set_animation(self, time: float):
        self.animation_time = time

    def set_recording_animation(self):
        self.recording_animation_time = 0

    def set_recording(self, recorded_points: list):
        self.recorded_points = recorded_points
        
    #return point that was clicked on, if any
    def get_selected_point(self, px, py):
        for p in self.key_points:
            pixel_pos = convert.meters_to_pixels((p.x, p.y), self.size)
            # vel_marker_pos = convert.meters_to_pixels(p.get_vel_marker_pos(), self.size)
            # if convert.get_dist(px, py, vel_marker_pos[0], vel_marker_pos[1]) <= 5:
            #     return None
            if convert.get_dist(px, py, pixel_pos[0], pixel_pos[1]) <= 7:
                self.selected_point = p
                return p
        return None

    def update(self, points: list, sampled_points: list, sample_rate: float, commands: list[dict]):
        self.key_points = points
        self.sampled_points = sampled_points
        self.sample_rate = sample_rate
        self.commands = commands

    def update_selected_point(self, point):
        self.selected_point = point

    def update_info(self):
        pos = convert.get_cursor_field_pos_meters(self.size)
        pixel_pos = convert.get_cursor_screen_pos_pixels()
        if self.selected_point != None:
            dist = convert.get_cursor_dist_meters([self.selected_point.x, self.selected_point.y], self.size)
            self.info_label.text = f"[b]PX:[/b] {pixel_pos[0]}, [b]PY:[/b]{pixel_pos[1]}\n[b]X:[/b] {round(pos[0], 3)}, [b]Y:[/b] {round(pos[1], 3)}\n[b]Dist:[/b] {round(dist, 3)}"
        else:
            self.info_label.text = f"[b]PX:[/b] {pixel_pos[0]}, [b]PY:[/b]{pixel_pos[1]}\n[b]X:[/b] {round(pos[0], 3)}, [b]Y:[/b] {round(pos[1], 3)}\n[b]Dist:[/b] null"
        texture = self.info_label.texture
        if texture == None:
            return
        self.info_rect = Rectangle(texture = texture, size = list(texture.size), pos = (35, 667))
        self.canvas.add(self.info_rect)