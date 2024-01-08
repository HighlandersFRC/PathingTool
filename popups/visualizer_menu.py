from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button

from tools import file_manager
import csv
from matplotlib import pyplot as plt

class VisualizerMenu(Popup):
    def __init__(self, display_func, sample_func, clear_local_func, clear_rio_func, **kwargs):
        super().__init__(title = "Visualizer Menu", **kwargs)

        self.display_func = display_func
        self.clear_local_func = clear_local_func
        self.clear_rio_func = clear_rio_func
        self.sample_func = sample_func

        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        self.data_chooser = FileChooserListView(path = "./recorded_data")
        self.controls_layout = BoxLayout(orientation = "horizontal", size_hint = (1, 0.1))
        self.layout.add_widget(self.data_chooser)
        self.layout.add_widget(self.controls_layout)

        self.graph_button = Button(text = "Graph", on_press = self.graph)
        self.display_on_field_button = Button(text = "Disp. on Field", on_press = self.display_on_field)
        self.clear_recording_on_field_button = Button(text = "Clear Rec. On Field", on_press = self.clear_recording_on_field, background_color = (1, 0, 0, 1))
        self.update_button = Button(text = "Update", on_press = self.update, background_color = (0, 1, 0, 1))
        self.clear_local_button = Button(text = "Clear Local Rec.", on_press = self.clear_local_recordings, background_color = (1, 0, 0, 1))
        self.clear_rio_button = Button(text = "Clear Rio Rec.", on_press = self.clear_rio_recordings, background_color = (0.5, 0, 0, 1))
        self.cancel_button = Button(text = "Back", on_press = self.cancel)
        self.controls_layout.add_widget(self.graph_button)
        self.controls_layout.add_widget(self.display_on_field_button)
        self.controls_layout.add_widget(self.clear_recording_on_field_button)
        self.controls_layout.add_widget(self.update_button)
        self.controls_layout.add_widget(self.clear_local_button)
        self.controls_layout.add_widget(self.clear_rio_button)
        self.controls_layout.add_widget(self.cancel_button)

    def on_open(self):
        self.data_chooser.path = "./recorded_data"

    def update(self, event):
        file_manager.download_recorded_data("10.44.99.2")
        self.data_chooser.path = "./recorded_data"
        self.data_chooser._update_files()
        self.data_chooser.path = "./recorded_data"

    def graph(self, event):
        if self.data_chooser.selection == []:
            return
        with open(self.data_chooser.selection[0], newline = "") as file:
            reader = csv.reader(file)
            recorded_data = [[float(val) for val in row] for row in list(reader)]
        plt.plot([row[0] for row in recorded_data], [row[1] for row in recorded_data], color = (0, 0, 1, 1), label = "X")
        plt.plot([row[0] for row in recorded_data], [row[2] for row in recorded_data], color = (0, 1, 0, 1), label = "Y")
        plt.plot([row[0] for row in recorded_data], [row[3] for row in recorded_data], color = (1, 0, 0, 1), label = "Theta")
        plt.xlabel("Time")
        plt.title("X, Y, Theta vs Time")
        plt.grid(visible = True, which = "both")
        plt.legend()
        plt.tight_layout()
        optimal_data = self.sample_func(times = True)
        if optimal_data != None:
            plt.plot([row[0] for row in optimal_data], [row[1] for row in optimal_data], color = (0, 0, 1, 0.5), label = "Opt. X")
            plt.plot([row[0] for row in optimal_data], [row[2] for row in optimal_data], color = (0, 1, 0, 0.5), label = "Opt. Y")
            plt.plot([row[0] for row in optimal_data], [row[3] for row in optimal_data], color = (1, 0, 0, 0.5), label = "Opt. Theta")
        plt.show()

    def display_on_field(self, event):
        if self.data_chooser.selection == []:
            return
        with open(self.data_chooser.selection[0], newline = "") as file:
            reader = csv.reader(file)
            data = [[float(val) for val in row] for row in list(reader)]
        self.display_func(data)
        self.dismiss()

    def clear_recording_on_field(self, event):
        self.display_func([[0, 0, 0]])
        self.dismiss()

    def clear_local_recordings(self, event):
        self.clear_local_func()
        self.data_chooser._update_files()
        self.data_chooser.path = "./recorded_data"

    def clear_rio_recordings(self, event):
        self.clear_rio_func()

    def cancel(self, event):
        self.dismiss()