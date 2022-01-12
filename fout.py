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

Builder.load_file('fout.kv')

class foutPopup(Popup):
    def __init__(self, **kwargs):
        super(foutPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.closeFoutPopup, 3)

    def closeFoutPopup(self, dt):
        self.dismiss()
        print('Het antwoord is fout, gebruiker heeft feedback gekregen')

class Widgets(Widget):
    def btn(self):
        popup = foutPopup()
        popup.open()

class MyApp(App):
    def build(self):
        return Widgets()   
    
            

if __name__ == "__main__":
    MyApp().run()

