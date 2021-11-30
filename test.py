import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Canvas
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

import serial
import time

Builder.load_file('info.kv');
Builder.load_file('error.kv')

voorwerpPlaatsen = [[1,0,1,1], [1,0,1,0]]

class RedCircle(Widget):
    pass

class GreenCircle(Widget):
    pass
class BackDrop(Widget):
    pass
class ErrorPopUp(Widget):
    tafel= ObjectProperty()
    tafel_1 = ObjectProperty()
    tafel_2 = ObjectProperty()
    tafel_3 = ObjectProperty()
    tafel_4 = ObjectProperty()


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
        #Clock.schedule_interval(self.timer, refresh_time)
        self.cols = 1


        self.info = GreenCircle();
        self.add_widget(self.info)
        self.checkErr()

    def checkErr(self):
        count = 0
        if sum(x.count(0) for x in voorwerpPlaatsen) > 1:
            self.clear_widgets();
            popupLayout = ErrorPopUp()

            #backdrop = BackDrop();
            #popupLayout.add_widget(backdrop)
            layout = GridLayout(cols= 4, size_hint=(0.6, 0.7))
            print(layout.size)
            with layout.canvas.before:
                Color(0, 1,  0, 0.25)
                Rectangle(size=(layout.size))
                print(layout.size)
            for rows in range(len(voorwerpPlaatsen)):
                for col in range(len(voorwerpPlaatsen[rows])):
                    if voorwerpPlaatsen[rows][col] == 0:
                        #layout.add_widget(RedCircle())
                        popupLayout.tafel.add_widget(RedCircle())
                        print(popupLayout.tafel.size)
                    else:
                        popupLayout.tafel.add_widget(GreenCircle())

            #popupLayout.add_widget(layout)
            #popupLayout.add_widget(Label(text="dit is een test"))
            self.add_widget(popupLayout)
        print(sum(x.count(0) for x in voorwerpPlaatsen))
        #print(len(voorwerpPlaatsen))

    def timer(self, dt):
        if ser.in_waiting > 2:

            line = ser.readline().decode('utf-8').rstrip();
            print(voorwerpPlaatsen[0])
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
