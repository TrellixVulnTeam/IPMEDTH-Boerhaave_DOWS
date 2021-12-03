from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Canvas
from kivy.properties import StringProperty, ObjectProperty

import serial
import time
import random

Builder.load_file('BasisSchermLayout.kv')
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
    pass
class InfoSaturnMoon(Widget):
    pass
class InfoMoon(Widget):
    pass
class Instruction(Widget):
    pass


class MyLayout(Widget):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        refresh_time = 0.5
        Clock.schedule_interval(self.timer, refresh_time)

    def press_it(self):
        current = self.ids.my_progress_bar.value
        current_question = self.ids.my_label.value

        if current == 1:
          current = 0

        if current_question == 5:
          current_question = 0

        current += .20
        current_question += 1

        self.question_choser()

        self.ids.my_progress_bar.value = current
        self.ids.my_label.value = current_question
        self.ids.my_label.text = f'Vraag {self.ids.my_label.value}'

    def question_choser(self):
        questions = ['vraag1: testen', 'vraag2: Hallo', 'vraag3: hoi', 'vraag4: doeg']

        while len(questions) > 0:
          index = random.choice(questions)
          self.ids.my_label_question.text = index
          questions.remove(index)
          print(questions)


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
            self.ids.info_scherm.clear_widgets()
            if nummerNFCreader == 0:
                self.ids.info_scherm.add_widget(InfoMoon())
            if nummerNFCreader == 1:
                self.ids.info_scherm.add_widget(InfoSaturnMoon())
            if nummerNFCreader == 2:
                print("test")
            if nummerNFCreader == 3:
                print("test")

    def antwoordBerichtChecken(self, message):
        #a_none
        if "none" in message:
            #TODO Antwoord weghalen van veld
            print("voorwerp opgetilt")
        #a_sn
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
                    self.ids.info_scherm.add_widget(InfoMoon())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 1:
                    self.ids.info_scherm.add_widget(InfoSaturnMoon())




class MyApp(App):
  def build(self):
    return MyLayout()


if __name__ == '__main__':
  Config.set('graphics', 'fullscreen', 'auto')
  Config.set('graphics', 'window_state', 'maximized')
  Config.write()
  #setup van de serial poort waar de pi naar luistert
  ser = serial.Serial('COM4', 9600, timeout=1)
  ser.reset_input_buffer()
  MyApp().run()
