import kivy
import random
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

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

Builder.load_file('my.kv')

class popupInhoudFout(FloatLayout):
    pass

class popupInhoudGoed(FloatLayout):
    pass

class MyGrid(GridLayout):
    def goed(self):
        show_popupGoed()
        GPIO.output(23,GPIO.HIGH)
        time.sleep(3)
        GPIO.output(23,GPIO.LOW)
    pass

    def fout(self):
        show_popupFout()
        GPIO.output(18,GPIO.HIGH)
        time.sleep(3)
        GPIO.output(18,GPIO.LOW)
    pass

def show_popupFout():
    show = popupInhoudFout()
    popupWindow = Popup(title='Test popup',content=Label(text='Hello world'),size_hint=(None, None), size=(400, 400))
    popupWindow.open()


def show_popupGoed():
    show = popupInhoudGoed()
    popupWindow = Popup(title='Test popup',content=Label(text='Hello world'),size_hint=(None, None), size=(400, 400))
    popupWindow.open()


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
