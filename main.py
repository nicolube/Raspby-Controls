from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

from kivy.lang import Builder, builder
from kivy.config import Config
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

from os import path

import flasher.flasher

__dir = path.dirname(path.realpath(__file__))


class MainScreen(Screen):
    pass


Builder.load_file(__dir+"/defaults.kv")
buildKv = Builder.load_file(__dir+"/main.kv")

class RaspyControllApp(App):
    def build(self):
        return buildKv

if __name__ == "__main__":
    RaspyControllApp().run()