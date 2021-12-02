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

voorwerpPlaatsen = [1,1,1,1,1,1,1,1]

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
        Clock.schedule_interval(self.timer, refresh_time)
        self.cols = 1


        self.info = GreenCircle();
        self.add_widget(self.info)
        #self.checkErr()

    def checkErr(self):
        count = 0
        if voorwerpPlaatsen.count(0) > 1:
            self.clear_widgets();
            popupLayout = ErrorPopUp()
            layout = GridLayout(cols= 4, size_hint=(0.6, 0.7))
            with layout.canvas.before:
                Color(0, 1,  0, 0.25)
                Rectangle(size=(layout.size))
            for rows in range(len(voorwerpPlaatsen)):
                if voorwerpPlaatsen[rows] == 0:
                    #layout.add_widget(RedCircle())
                    popupLayout.tafel.add_widget(RedCircle())
                else:
                    popupLayout.tafel.add_widget(GreenCircle())

            self.add_widget(popupLayout)

    #timer function die checkt of er een bericht van de arduino binnen is
    def timer(self, dt):
        if ser.in_waiting > 2:
            line = ser.readline().decode('utf-8').rstrip();
            self.arduinoCheck(line)

    #als een voorwerp wordt opgepakt, checkt welk voorwerp het is en of er teveel zijn opgetild
    def optillenVoorwerpCheck(self, nummerNFCreader):
        voorwerpPlaatsen[nummerNFCreader] = 0
        if voorwerpPlaatsen.count(0) > 1:
            self.checkErr()
        else:
            self.clear_widgets()
            if nummerNFCreader == 0:
                self.add_widget(InfoMoon())
            if nummerNFCreader == 1:
                self.add_widget(InfoSaturnMoon())
            if nummerNFCreader == 2:
                print("test")
            if nummerNFCreader == 3:
                print("test")

    def antwoordBerichtChecken(self, message):
        if "none" in message:
            #TODO Antwoord weghalen van veld
            print("voorwerp opgetilt")
        elif "sn" in message:
            #TODO ALLE ANTWOORDEN TOEVOEGEN
            print("antwoord")

    def arduinoCheck(self, message):
        if(message[0] == 'a'):
            self.antwoordBerichtChecken(message)
        else:
            try:
                print(message)
                numberReader = int(message[0])
                if "none" in message:
                    self.optillenVoorwerpCheck(numberReader)
                #checks of het voorwerp dat neergezet wordt, overheen komt met wat er hoort te staan
                elif numberReader == 0:
                    if "sn" in message:
                        self.clear_widgets()
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 1:
                    if "mn" in message:
                        self.clear_widgets()
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
            except:
                print("verkeerde input")


    #als een voorwerp terug gezet wordt, check of er nog één voorwerp vast wordt gehouden, zoja, geef info weer
    def terugzettenErrorCheck(self):
        if voorwerpPlaatsen.count(0) < 2:
            for nfcreader in range(len(voorwerpPlaatsen)):
                if voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 0:
                    self.add_widget(InfoMoon())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 1:
                    self.add_widget(InfoSaturnMoon())






class MyApp(App):
    def build(self):
        Window.clearcolor = (0,0,0,1)
        return MyGrid()

if __name__ == "__main__":
    #setup van de serial poort waar de pi naar luistert
    ser = serial.Serial('COM4', 9600, timeout=1)
    ser.reset_input_buffer()
    MyApp().run()
