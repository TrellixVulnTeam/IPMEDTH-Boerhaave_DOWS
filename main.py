from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle, Canvas
from kivy.properties import StringProperty, ObjectProperty

import serial
import time
import random

Builder.load_file('BasisSchermLayout.kv')
Builder.load_file('info.kv')
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
    backgrounderror = ObjectProperty()
    pass
class InfoSaturnMoon(Widget):
    pass
class InfoTelescoop(Widget):
    pass
class InfoJupiter(Widget):
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
        self.popup = ModalView(size_hint=(None, None))

    def press_it(self):
        current = self.ids.my_progress_bar.value
        current_question = self.ids.my_label.value

        if current == 1:
          current = 0

        if current_question == 5:
          current_question = 0

        current += .20
        current_question += 1

        self.ids.info_scherm.clear_widgets()
        self.ids.info_scherm.add_widget(InfoMoon())

        self.question_choser()

        self.ids.my_progress_bar.value = current
        self.ids.my_label.value = current_question
        self.ids.my_label.text = f'Vraag {self.ids.my_label.value}'

    def question_choser(self):
        questions = ['nieuwe_vraag1', 'nieuwe_vraag2', 'nieuwe_vraag3', 'nieuwe_vraag4']

        while len(questions) > 0:
          index = random.choice(questions)
          questions.remove(index)
          print(questions)


    #checkt of er een error is, als er meer dan 2 voorwerpen zijn opgetild
    def checkErr(self):
        if voorwerpPlaatsen.count(0) > 1:
            #checkt of een popup momenteel open is, zo ja, doet het dicht
            if isinstance(App.get_running_app().root_window.children[0], Popup):
                App.get_running_app().root_window.children[0].dismiss()
            #maakt de layout van de pop
            popupLayout = ErrorPopUp()
            layout = GridLayout(cols= 4, size_hint=(0.6, 0.7))
            #voegt de achtergrond toe aan de popup
            with layout.canvas.before:
                Color(0, 1,  0, 0.25)
                Rectangle(size=(layout.size))
            #loopt door alle voorwerpen heen. Als een vorwerp is opgetild rood cirkel anders groen
            for rows in range(len(voorwerpPlaatsen)):
                if voorwerpPlaatsen[rows] == 0:
                    popupLayout.tafel.add_widget(RedCircle())
                else:
                    popupLayout.tafel.add_widget(GreenCircle())

            #self.popup = ModalView(size_hint=(None, None))
            with popupLayout.backgrounderror.canvas.before:
                Color(0.1,0.1,0.1, 1)
                Rectangle(pos=(self.center_x / 2, self.center_y / 2), size=(self.size[0] / 2, self.size[1] / 2))
            popupLayout.backgrounderror.size = self.size[0] / 2, self.size[1] / 2
            popupLayout.backgrounderror.pos = self.center_x / 2, self.center_y / 2
            self.popup.add_widget(popupLayout)
            self.popup.open()

    #timer function die checkt of er een bericht van de arduino binnen is
    def timer(self, dt):
        if ser.in_waiting > 2:
            line = ser.readline().decode('utf-8').rstrip()
            self.arduinoCheck(line)

    #als een voorwerp wordt opgepakt, checkt welk voorwerp het is en of er teveel zijn opgetild
    def optillenVoorwerpCheck(self, nummerNFCreader):
        voorwerpPlaatsen[nummerNFCreader] = 0
        #als er meer dan 2 voorwerpen zijn opgetilt, ga naar error scherm
        if voorwerpPlaatsen.count(0) > 1:
            self.checkErr()
        #anders kijk welk voorwerp is opgetild en laat de info scherm zin
        else:
            self.ids.info_scherm.clear_widgets()
            if nummerNFCreader == 0:
                self.ids.info_scherm.add_widget(InfoMoon())
            if nummerNFCreader == 1:
                self.ids.info_scherm.add_widget(InfoSaturnMoon())
            if nummerNFCreader == 2:
                self.ids.info_scherm.add_widget(InfoTelescoop())
            if nummerNFCreader == 3:
                self.ids.info_scherm.add_widget(InfoJupiter())

    #functie die checkt wat voor antwoord bericht er van de arduino wordt verstuurd
    def antwoordBerichtChecken(self, message):
        #a_none
        if "none" in message:
            #TODO Antwoord weghalen van veld
            print("voorwerp opgetilt")
        #a_sn
        elif "sn" in message:
            #TODO ALLE ANTWOORDEN TOEVOEGEN
            print("antwoord")

    #checkt het bericht dat de machine krijgt van de Arduino
    def arduinoCheck(self, message):
        #als het met een a begint, dan gaat het om de antwoord reader
        if(message[0] == 'a'):
            self.antwoordBerichtChecken(message)
        elif(message == "reset"):
            print("reset")
        else:
            #filtert op slechte inputs. Alleen inputs van de arduino dat begint met een nummer of a worden toegelaten
            try:
                print(message)
                numberReader = int(message[0])
                #een x_none bericht geeft aan dat een voorwerp is opgeteld op reader x (x = nummer)
                if "none" in message:
                    self.optillenVoorwerpCheck(numberReader)
                #checks of het voorwerp dat neergezet wordt, overheen komt met wat er hoort te staan
                elif numberReader == 0:
                    if "mn" in message:
                    #    self.ids.info_scherm.clear_widgets()
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 1:
                    if "sn" in message:
                        print("in")
                    #    self.ids.info_scherm.clear_widgets()
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 2:
                    if "ts" in message:
                    #    self.ids.info_scherm.clear_widgets()
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 3:
                    if "jm" in message:
                    #    self.ids.info_scherm.clear_widgets()
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
            except Exception as e:
                print("verkeerde input")
                print(e)


    #als een voorwerp terug gezet wordt, check of er nog één voorwerp vast wordt gehouden, zoja, geef info weer
    def terugzettenErrorCheck(self):
        if voorwerpPlaatsen.count(0) < 2:
            self.popup.dismiss()
            #loopt door de voorwerpen array heen en laat de informatie zien van één voorwerp dat opgetilt is
            for nfcreader in range(len(voorwerpPlaatsen)):
                if voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 0:
                    self.ids.info_scherm.clear_widgets()
                    self.ids.info_scherm.add_widget(InfoMoon())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 1:
                    self.ids.info_scherm.clear_widgets()
                    self.ids.info_scherm.add_widget(InfoSaturnMoon())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 2:
                    self.ids.info_scherm.clear_widgets()
                    self.ids.info_scherm.add_widget(InfoTelescoop())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 3:
                    self.ids.info_scherm.clear_widgets()
                    self.ids.info_scherm.add_widget(InfoJupiter())
        else:
            self.checkErr()




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
