from sys import platform
from kivy import app
from kivy import lang
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooser
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from os import path
from pathlib import Path
import os
import util
from platformio.project.config import ProjectConfig

config = util.config["flasher"]

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
    select_button = ObjectProperty(None)
    environment_spinner:  ObjectProperty(None)
    upload_port = None
    project_config = None

    def on_enter(self):
        super().on_enter(self)

    def select(self, port):
        pass

    def set_upload_port(self, port):
        self.upload_port = port
    def update_project_path(self, _, sel):
        self.select_button.text = path.basename(sel)
        self.project_config = ProjectConfig(path.join(sel, "platformio.ini"))
        envs = self.project_config.envs()
        self.environment_spinner.values = envs
        dEnvs = self.project_config.default_envs()
        self.environment_spinner.disabled = False
        if len(dEnvs) > 0:
            self.environment_spinner.text = dEnvs[0]
        elif len(envs) > 0:
            self.environment_spinner.text = envs[0]
        else:
            self.environment_spinner.text = "No Envs!"
            self.environment_spinner.disabled = True


class SerialSpinner(Spinner):
    def refresh(self):
        self.values = util.serial_ports()

class DriveSipinner(Spinner):
    def refresh(self):
        self.values = util.drives()
        self.values.append("Home")


class PioFileChooserScreen(Screen):
    file_chooser = ObjectProperty(None)
    drive_select = ObjectProperty(None)
    def on_pre_enter(self):
        self.file_chooser.rootpath = config["firmwarePath"]
    global data
    def entityProcessor(self, entry, parent):
        c = parent.children[0].children
        if c[0].text == "":
            if path.exists(path.join(self.file_chooser.path, c[1].text, "platformio.ini")):
                c[1].color = (1, .5, 0, 1)
                parent.locked = True
    def update_drives(self):
        drives = ["Home"]
        for d in util.drives():
            drives.append(d)
        self.drive_select.values = drives
    def select_root_path(self, pKey):
        if (pKey == "Home"):
            self.file_chooser.rootpath = config["firmwarePath"]
            return
        self.file_chooser.rootpath = path.join(util.drive_basepath, pKey)
    def on_touch(self, s, t):
        if not s or not path.isdir(s[0]):
            return
        if self.is_pio_project(s[0]) and t.is_double_tap:
            t.is_double_tap = False
            self.file_chooser.cancel()
            #self.file_chooser.path = path.join(self.file_chooser.path, os.pardir

    def is_pio_project(self, file):
        if not path.isdir(file):
            return False
        for fn in os.listdir(file):
            if path.basename(fn) == "platformio.ini":
                return True
        return False
    def is_pio_project_selection(self, selection):
        if len(selection) > 0:
            if self.is_pio_project(selection[0]):
                return True
        return False