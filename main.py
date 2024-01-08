from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from pathtool import PathTool
import pyautogui

TITLE = "2023 Path Tool - Highlanders FRC #4499"
ICON = "images/4499Icon.ico"

class PathApp(App):
    def build(self):
        #schedule execute callback
        Clock.schedule_interval(self.execute, 1.0  / 60.0)
        self.title = TITLE
        self.icon = ICON
        self.path_tool = PathTool()
        Window.maximize()
        return self.path_tool

    #called at 60 Hz by Clock
    def execute(self, dt):
        self.path_tool.path.draw_path(dt)
        self.path_tool.editor.save_load.update()

if __name__ == "__main__":
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    PathApp().run()