from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class SaveLoad(Popup):
    def __init__(self, save_func, load_func, upload_func, upload_all_func, download_all_func, **kwargs):
        super().__init__(title = "Save or Load path file", **kwargs)

        #save or load
        self.mode = "save"

        #callback functions
        self.save_func = save_func
        self.load_func = load_func
        self.upload_func = upload_func
        self.upload_all_func = upload_all_func
        self.download_all_func = download_all_func

        #main layout
        self.layout = BoxLayout(orientation = "vertical")
        self.add_widget(self.layout)

        #sub-layout for text box
        self.controls_layout = BoxLayout(orientation = "horizontal", size_hint = (1, 0.16))
        #sub-layout for buttons
        self.buttons_layout = GridLayout(cols = 3)

        #Create and add widgets
        self.file_chooser = FileChooserListView(path = "./saves")
        self.text_box = TextInput(hint_text = "File name")
        self.sample_rate_input = TextInput(hint_text = "Sample rate (sec)", text = "0.01", input_filter = "float", size_hint = (0.2, 1))
        self.load_button = Button(text = "Load", on_press = self.load)
        self.save_button = Button(text = "Save", on_press = self.save)
        self.cancel_button = Button(text = "Cancel", on_press = self.cancel)
        self.upload_button = Button(text = "Upload", on_press = self.upload)
        self.upload_all_button = Button(text = "Upload All", on_press = self.upload_all)
        self.download_all_button = Button(text = "Download All", on_press = self.download_all)
        self.path_label = Label(text = "", size_hint = (1, 0.05))
        self.layout.add_widget(self.path_label)
        self.layout.add_widget(self.file_chooser)
        self.layout.add_widget(self.controls_layout)
        self.controls_layout.add_widget(self.text_box)
        self.controls_layout.add_widget(self.sample_rate_input)
        self.buttons_layout.add_widget(self.upload_button)
        self.buttons_layout.add_widget(self.upload_all_button)
        self.buttons_layout.add_widget(self.download_all_button)
        self.buttons_layout.add_widget(self.load_button)
        self.buttons_layout.add_widget(self.save_button)
        self.buttons_layout.add_widget(self.cancel_button)
        self.controls_layout.add_widget(self.buttons_layout)

    #save path
    def save(self, event):
        if not "saves" in self.file_chooser.path or self.text_box.text == "" or self.sample_rate_input.text == "":
            return
        self.save_func(self.file_chooser.path, self.text_box.text, float(self.sample_rate_input.text))
        self.dismiss()

    #load path
    def load(self, event):
        if not "saves" in self.file_chooser.path or self.file_chooser.selection == []:
            return
        self.load_func(self.file_chooser.selection[0])
        self.dismiss()

    #do nothing and close popup
    def cancel(self, event):
        self.dismiss()

    #upload current path
    def upload(self, event):
        if not "saves" in self.file_chooser.path or self.text_box.text == "" or self.sample_rate_input.text == "":
            return
        if self.file_chooser.selection == []:
            self.file_chooser.selection.append(f"{self.file_chooser.path}\\{self.text_box.text}.json")
        self.upload_func(self.file_chooser.selection[0], self.file_chooser.path, self.text_box.text, float(self.sample_rate_input.text))
        self.dismiss()

    #upload all paths
    def upload_all(self, event):
        if not "saves" in self.file_chooser.path or self.text_box.text == "" or self.sample_rate_input.text == "":
            return
        if self.file_chooser.selection == []:
            self.file_chooser.selection.append(f"{self.file_chooser.path}\\{self.text_box.text}.json")
        self.upload_all_func(self.file_chooser.path, self.text_box.text, float(self.sample_rate_input.text))
        self.dismiss()

    #download all paths
    def download_all(self, event):
        self.download_all_func()
        self.dismiss()

    #update callback
    def update(self):
        self.path_label.text = self.file_chooser.path
        if self.mode == "save":
            pass
        elif self.mode == "load":
            if len(self.file_chooser.selection) > 0:
                self.text_box.text = self.file_chooser.selection[0]