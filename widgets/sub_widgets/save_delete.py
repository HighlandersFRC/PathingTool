from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class SaveDelete(BoxLayout):
    def __init__(self, delete_point, clear_points, save_func, load_func, upload_func, **kwargs):
        super().__init__(**kwargs)
        #callback functions
        self.delete_point = delete_point
        self.clear_points = clear_points
        self.save_func = save_func
        self.load_func = load_func
        self.upload_func = upload_func

        #create and add sub-widgets
        self.clear_button = Button(text = "CLEAR", background_color = (0.5, 0, 0, 1), on_press = self.clear)
        self.delete_button = Button(text = "DELETE", background_color = (1, 0, 0, 1), on_press = self.delete)
        self.save_button = Button(text = "SAVE", background_color = (0, 0.5, 0, 1), on_press = self.save)
        self.load_button = Button(text = "LOAD", background_color = (0, 1, 0, 1), on_press = self.load)
        self.upload_download_button = Button(text = "UP/DOWNLOAD", background_color = (0, 0.5, 0, 1), on_press = self.upload, size_hint = (1.5, 1))
        self.add_widget(self.clear_button)
        self.add_widget(self.delete_button)
        self.add_widget(self.save_button)
        self.add_widget(self.load_button)
        self.add_widget(self.upload_download_button)

    #updload button callback
    def upload(self, event):
        self.upload_func()

    #save button callback
    def save(self, event):
        self.save_func()

    #load button callback
    def load(self, event):
        self.load_func()

    #delete button callback
    def delete(self, event):
        self.delete_point()

    #clear button callback
    def clear(self, event):
        self.clear_points()