from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from SplineGeneration.generatePolarSplines import SplineGenerator
from tools import convert
from kivy.graphics import *
import math
import random

class ArmAnimation(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)

        #main widgets
        self.animation = Image()

        #add main widgets
        self.add_widget(self.animation)

        self.spline_generator = SplineGenerator()

        #physical constants (s, deg, in)
        self.UPRIGHT_ARM_ANGLE = 180
        self.MIN_ARM_LENGTH = 12
        self.MAX_ARM_LENGTH = 80

        #setpoints
        #[time (s), arm angle (deg), arm extension (in)]
        # self.setpoints = [
        #     [0, 180, 0, 0, 0, 0, 0],
        #     [0.5, 180, 40, 0, 0, 0, 0],
        #     [1, 180, 0, 0, 0, 0, 0],
        #     [1.5, 135, 0, 0, 0, 0, 0],
        #     [2, 180, 0, 0, 0, 0, 0],
        #     [2.5, 135, 40, 0, 0, 0, 0],
        #     [3, 225, 20, 0, 0, 0, 0],
        #     [3.5, 180, 0, 0, 0, 0, 0]
        # ]
        self.setpoints = [[i / 2, random.randint(80, 280), random.randint(0, 50), 0, 0, 0, 0] for i in range(100)]
        self.anim_time = 0
        self.angle = 180
        self.extension = 0
        self.spline_generator.generateSplineCurves(self.setpoints)

        self.anim_group = InstructionGroup()
        self.scale_factor = 7
        self.pivot_pos = [800, 200]

    def update(self, dt: float):

        pos = self.spline_generator.sample_pos(self.setpoints, self.anim_time)
        self.extension = pos[1]
        self.angle = pos[0]
        self.anim_time += dt
        if self.anim_time > self.setpoints[-1][0]:
            self.anim_time = 0
        # print(f"Time: {self.anim_time}")
        # print(f"Ext: {self.extension}")
        # print(f"Ang: {self.angle}")

        self.anim_group.clear()
        self.canvas.clear()

        self.anim_group.add(Color(3 / 255, 252 / 255, 244 / 255, 1))
        self.anim_group.add(Line(points = [self.pivot_pos[0], self.pivot_pos[1], self.scale_factor * (self.extension + self.MIN_ARM_LENGTH) * math.cos(convert.deg_to_rad(self.angle - 90)) + self.pivot_pos[0], self.scale_factor * (self.extension + self.MIN_ARM_LENGTH) * math.sin(convert.deg_to_rad(self.angle - 90)) + self.pivot_pos[1]], width = self.scale_factor, cap = "square", joint = "miter"))
        self.anim_group.add(Color(0.75, 0.75, 0.75))
        self.anim_group.add(Line(points = [self.pivot_pos[0], self.pivot_pos[1], self.scale_factor * (self.MIN_ARM_LENGTH) * math.cos(convert.deg_to_rad(self.angle - 90)) + self.pivot_pos[0], self.scale_factor * (self.MIN_ARM_LENGTH) * math.sin(convert.deg_to_rad(self.angle - 90)) + self.pivot_pos[1]], width = self.scale_factor, cap = "square", joint = "miter"))

        self.canvas.add(self.anim_group)