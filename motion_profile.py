from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from tools.motion_profile.arm_animation import ArmAnimation


TITLE = "2023 Arm Motion Profile Simulator - Highlanders FRC #4499"
ICON = "images/4499Icon.ico"

class MotionProfileApp(App):
    def build(self):
        Clock.schedule_interval(self.execute, 1 / 60)
        self.title = TITLE
        self.icon = ICON
        self.arm_animation = ArmAnimation()
        Window.maximize()
        return self.arm_animation

    def execute(self, dt):
        self.arm_animation.update(dt)

if __name__ == "__main__":
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    MotionProfileApp().run()