import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Canvas
from kivy.lang import Builder

import serial
import time

Builder.load_file('info.kv');
Builder.load_file('error.kv')

class ErrorPopUp(Widget):
    pass

class InfoSaturnMoon(Widget):
    pass

class InfoMoon(Widget):
    pass

class Instruction(Widget):
    pass

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        refresh_time = 0.5
        Clock.schedule_interval(self.timer, refresh_time)
        self.cols = 1
        self.info = Instruction();
        self.add_widget(self.info)

    def timer(self, dt):
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip();
            print(line);
            if "sn" in line:
                self.clear_widgets()
                self.add_widget(InfoSaturnMoon())
            if "mn" in line:
                self.clear_widgets()
                self.add_widget(InfoMoon())



class MyApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return MyGrid()

if __name__ == "__main__":
    ser = serial.Serial('COM4', 9600, timeout=1)
    ser.reset_input_buffer()
    MyApp().run()
