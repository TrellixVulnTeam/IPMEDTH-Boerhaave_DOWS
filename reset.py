import kivy
import random
import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock

Builder.load_file('reset.kv')

class ResetPopup(Popup):
    def __init__(self, **kwargs):
        super(ResetPopup, self).__init__(**kwargs)
        # call dismiss_popup in 2 seconds
        Clock.schedule_once(self.restarting_App, 5)

    def restarting_App(self, dt):
        App.get_running_app().restart()
        print('Applicatie is gerestart')

class Widgets(Widget):
    def btn(self):
        popup = ResetPopup()
        popup.open()

class MyApp(App):
    def build(self):
        return Widgets()
    
    def restart(self):
        self.root.clear_widgets()
        self.stop()
        return MyApp().run()
            

if __name__ == "__main__":
    MyApp().run()
