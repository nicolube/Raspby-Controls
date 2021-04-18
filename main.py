from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.core.window import Window

from kivy.lang import Builder
from kivy.config import Config
from subprocess import call

from os import path

import flasher.flasher

#Window.show_cursor = False

#Window.size = (800, 480)

__dir = path.dirname(path.realpath(__file__))

class MainScreen(Screen):
    def on_shutdown(self):
        call("sudo poweroff", shell=True)


Builder.load_file(__dir+"/defaults.kv")
buildKv = Builder.load_file(__dir+"/main.kv")

class RaspyControllApp(App):
    def build(self):
        return buildKv

if __name__ == "__main__":
    RaspyControllApp().run()