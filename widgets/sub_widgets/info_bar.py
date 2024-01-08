from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class InfoBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)

        self.status_label = Label(text = "", markup = True, font_size = 24)
        self.time_label = Label(text = "[b]Total Time: 0.0[/b]", markup = True, font_size = 24, color = (27 / 255, 178 / 255, 181 / 255), size_hint = (0.6, 1))
        self.add_widget(self.status_label)
        self.add_widget(self.time_label)

    def update_status(self, text: str, color: tuple[float | int]):
        self.status_label.text = text
        self.status_label.color = color

    def update_time(self, time: float):
        self.time_label.text = f"[b]Total Time {round(time, 2)}[/b]"