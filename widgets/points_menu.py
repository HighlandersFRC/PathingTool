from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button

from data_assets.point import Point
from functools import partial

class PointsMenu(BoxLayout):
    def __init__(self, update_func, **kwargs):
        super().__init__(orientation = "vertical", **kwargs)
        #key points
        self.key_points = []
        #selected key point
        self.selected_point = None
        #update callback
        self.update_func = update_func

        #list of buttons
        self.buttons = []

    #update list of buttons  
    def update(self, key_points: list, selected_point: Point):
        self.clear_widgets()
        self.key_points = key_points
        self.selected_point = selected_point
        self.buttons = []
        for p in self.key_points:
            if selected_point != None:
                if selected_point.index == p.index:
                    self.buttons.append(MenuButton(p.index, "down", partial(self.select, p.index), self.move))
                else:
                    self.buttons.append(MenuButton(p.index, "normal", partial(self.select, p.index), self.move))
            else:
                self.buttons.append(MenuButton(p.index, "normal", partial(self.select, p.index), self.move))
        for b in self.buttons:
            self.add_widget(b)

    #button callback
    def select(self, index: int, event):
        self.selected_point = self.key_points[index]
        self.update_func(self.key_points, self.selected_point, update_equations = False)
        return index

    #index adjust callback
    def move(self, direction: int, event):
        #prevent errors
        if self.selected_point == None:
            return
        if self.selected_point.index == 0 and direction == -1:
            return
        elif self.selected_point.index == len(self.key_points) - 1 and direction == 1:
            return
        #switch points and update indexes and delta times
        self.selected_point.index += direction
        moved_point = self.key_points[self.selected_point.index]
        moved_point.index -= direction
        selected_point_dt = self.selected_point.delta_time
        self.selected_point.delta_time = moved_point.delta_time
        moved_point.delta_time = selected_point_dt
        self.key_points[self.selected_point.index] = self.selected_point
        self.key_points[moved_point.index] = moved_point
        self.update_func(self.key_points, self.selected_point)
        

#custom button for selecting points and adjusting indexes
class MenuButton(BoxLayout):
    def __init__(self, index: int, state: str, point_func, move_func, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)
        #layout for index adjusting buttons
        self.arrow_layout = BoxLayout(orientation = "vertical", size_hint = (0.4, 1))
        #index adjusting buttons
        self.up_button = Button(text = "[b]+[/b]", on_press = partial(move_func, 1), markup = True)
        self.down_arrow = Button(text = "[b]-[/b]", on_press = partial(move_func, -1), markup = True)
        #add index button
        self.arrow_layout.add_widget(self.down_arrow)
        self.arrow_layout.add_widget(self.up_button)
        #select point button
        self.point_button = ToggleButton(text = f"Point {index}", state = state, on_press = point_func)
        #add select point button and index buttons
        self.add_widget(self.point_button)
        self.add_widget(self.arrow_layout)