import math

class Point:
    def __init__(self, index: int, delta_time: float, x: float, y: float, angle: float, v_mag: float, v_theta: float, v_ang: float):
        #index in point list
        self.index = index
        #time from previous point
        self.delta_time = delta_time
        #absolute time in path
        self.time = 0.0
        #x and y position (meters)
        self.x = x
        self.y = y
        #angle (radians)
        self.angle = angle
        #velocity magnitude component (meters per second)
        self.velocity_magnitude = v_mag
        #velocity theta component (radians)
        self.velocity_theta = v_theta
        #angular velocity (radians per second)
        self.angular_velocity = v_ang
        
    def set_angle_degrees(self, degrees: float):
        self.angle = degrees * (math.pi / 180.0)

    def get_angle_degrees(self):
        return self.angle * (180.0 / math.pi)

    def set_vel_theta_degrees(self, degrees: float):
        self.velocity_theta = degrees * (math.pi / 180.0)

    def set_angular_velocity_degrees(self, degrees_per_second):
        self.angular_velocity = degrees_per_second * (math.pi / 180)

    def get_angular_velocity_degrees(self):
        return self.angular_velocity * (180 / math.pi)

    def get_vel_theta_degrees(self):
        return self.velocity_theta * (180.0 / math.pi)

    def get_vel_marker_pos(self):
        return self.x + self.velocity_magnitude * math.cos(self.velocity_theta), self.y + self.velocity_magnitude * math.sin(self.velocity_theta)

    def to_json(self):
        return self.__dict__