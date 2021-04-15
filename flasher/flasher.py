from sys import platform
from kivy import app
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooser
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Rectangle, Canvas
from os import path
from pathlib import Path
import os

from kivy.utils import rgba
import util

config = util.config["flasher"]
0
if config["firmwarePath"] == None:
    config["firmwarePath"] = str(Path().home())

__dir = path.dirname(path.realpath(__file__))

Builder.load_file(path.join(__dir, "flasher.kv"))

data = {
    "pio": path.join(__dir, "pics", "pio.png")
}

class FlasherMainScreen(Screen):
    port_select = ObjectProperty(None)
    popup = ObjectProperty(None)
    upload_port = None

    def on_enter(self):
        super().on_enter(self)

    def select(self, port):
        print(port)

    def set_upload_port(self, port):
        self.upload_port = port


class SerialSpinner(Spinner):
    def refresh(self):
        self.values = serial_ports()

class DriveSipinner(Spinner):
    def refresh(self):
        self.values = serial_ports()


class PioFileChooserScreen(Screen):
    file_chooser = ObjectProperty(None)
    drive_select = ObjectProperty(None)
    def on_pre_enter(self):
        self.file_chooser.rootpath = config["firmwarePath"]
        self.drive_select.values = util.find_usb_mass_storage()
    global data
    def entityProcessor(self, entry, parent):
        c = parent.children[0].children
        if c[0].text == "":
            if path.exists(path.join(self.file_chooser.path, c[1].text, "platformio.ini")):
                c[1].color = (1, .5, 0, 1)
                parent.locked = True
    def update_drives():
        
    def on_touch(self, s, t):
        if not s or not path.isdir(s[0]):
            return
        for fn in os.listdir(s[0]):
            if path.basename(fn) =="platformio.ini" and t.is_double_tap:
                t.is_double_tap = False
                self.file_chooser.cancel()
                #self.file_chooser.path = path.join(self.file_chooser.path, os.pardir)
                break