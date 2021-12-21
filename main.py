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

"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led_antwoord_goed = 20
led_antwoord_fout = 16
led_mn = 26
led_sn = 19
led_ts = 13
led_jm = 6
led_sc = 5
led_rs = 21
GPIO.setup(led_antwoord_goed, GPIO.OUT)
GPIO.setup(led_antwoord_fout, GPIO.OUT)
GPIO.setup(led_mn, GPIO.OUT)
GPIO.setup(led_sn, GPIO.OUT)
GPIO.setup(led_ts, GPIO.OUT)
GPIO.setup(led_jm, GPIO.OUT)
GPIO.setup(led_sc, GPIO.OUT)
GPIO.setup(led_rs, GPIO.OUT)
"""


Builder.load_file('BasisSchermLayout.kv')
Builder.load_file('info.kv')
Builder.load_file('error.kv')
Builder.load_file('victory.kv')
Builder.load_file('restart.kv')

voorwerpPlaatsen = [1,1,1,1,1,1]
voorwerpNamen = ["Maan Kraters", "Maan Saturnus", "Telescoop", "Manen Jupiter", "Sun-centered", "Ringen Saturnus"]
#questions = [['vraag1', 'mn'],
 # ['vraag2', 'mn'],
 # ['vraag3', 'sn'],
 # ['vraag4', 'sn'],
 # ['vraag5', 'ts'],
  #['vraag6', 'ts'],
  #['vraag7', 'jm'],
 # ['vraag8', 'jm'],
 # ['vraag9', 'sc'],
 # ['vraag10', 'sc'],
 # ['vraag11', 'rs'],
 # ['vraag12', 'rs']]
questions = ['vraag1','vraag2','vraag3','vraag4','vraag5','vraag6','vraag7','vraag8','vraag9','vraag10','vraag11','vraag12']
#antwoordeVragen = ['mn','mn','sn','sn','ts','ts','jm','jm','sc','sc','rs','rs']
antwoordeVragen = ['ts','ts','ts','ts','ts','ts','ts','ts','ts','ts','ts','ts']

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
class InfoSunCentered(Widget):
    pass
class InfoRings(Widget):
    pass
class Instruction(Widget):
    pass
class VictoryPopup(Widget):
    pass
class RestartPopup(Widget):
    pass



class MyLayout(Widget):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        #init vragen
        self.vragen = self.tienrandom()
        self.ids.my_label_question.text = self.vragen[0]
        #set timer voor arduino
        refresh_time = 0.5
        Clock.schedule_interval(self.timer, refresh_time)
        self.popup = ModalView(size_hint=(None, None))

        #bezig
        self.reset_timer = Clock.create_trigger(self.testing, 4)
        self.reset_timer()
        self.myTime = 0
        Clock.schedule_interval(self.increaseTimer, 1)

    def testing(self, dt):
        print(self.myTime)
        print("test")

    def increaseTimer(self, dt):
        self.myTime += 1

    def press_it(self):
        current = self.ids.my_progress_bar.value
        current_question = self.ids.my_label.value

        if current == 1:
          current = 0

        if current_question == 5:
          current_question = 0

        current += .20
        current_question += 1
        #delete de voorste vraag en pakt set de label voor nieuwe vraag
        self.vragen.pop(0)
        self.ids.my_label_question.text = self.vragen[0]

        self.ids.my_progress_bar.value = current
        self.ids.my_label.value = current_question
        self.ids.my_label.text = f'Vraag {self.ids.my_label.value} / 5'

    def tienrandom(self):
      randomvragen = []
      maximum_questions = 5
      randomlist = random.sample(range(0, len(questions)), maximum_questions)
      for item in randomlist:
        randomvragen.append(questions[item])
      return randomvragen


    def create_Victory_Popup(self):
        print("in")
        victoryPopup = VictoryPopup()
        with victoryPopup.ids.victoryLayout.canvas.before:
            Color(0.1,0.1,0.1, 1)
            Rectangle(pos=(self.center_x / 2, self.center_y / 2), size=(self.size[0] / 2, self.size[1] / 2))
        print("init")
        victoryPopup.ids.victoryLayout.size = self.size[0] / 2, self.size[1] / 2
        victoryPopup.ids.victoryLayout.pos = self.center_x / 2, self.center_y / 2
        return victoryPopup

    def createRestartPopup(self):
        restartPopup = RestartPopup()
        with restartPopup.ids.restartLayout.canvas.before:
            Color(0.1,0.1,0.1, 1)
            Rectangle(pos=(self.center_x / 2, self.center_y / 2), size=(self.size[0] / 2, self.size[1] / 2))
        restartPopup.ids.restartLayout.size = self.size[0] / 2, self.size[1] / 2
        restartPopup.ids.restartLayout.pos = self.center_x / 2, self.center_y / 2
        return restartPopup

    def closePopup(self, dt):
        self.victoryScreen.dismiss()

    def next_question(self):
        if len(self.vragen) > 1:
            current = self.ids.my_progress_bar.value
            current_question = self.ids.my_label.value

            if current == 1:
              current = 0

            if current_question == 5:
              current_question = 0

            current += .20
            current_question += 1
            #delete de voorste vraag en pakt set de label voor nieuwe vraag
            self.vragen.pop(0)
            self.ids.my_label_question.text = self.vragen[0]

            self.ids.my_progress_bar.value = current
            self.ids.my_label.value = current_question
            self.ids.my_label.text = f'Vraag {self.ids.my_label.value} / 5'
        else:
            #maakt de victory popup TODO: Layout maken
            self.victoryScreen = ModalView(size_hint=(None, None))
            self.victoryScreen.add_widget(self.create_Victory_Popup())
            self.victoryScreen.open()
            #automisch de popup weghalen na 5 seconden
            Clock.schedule_once(self.closePopup, 5)

            #restart
            self.vragen = self.tienrandom()
            self.ids.my_label_question.text = self.vragen[0]
            self.ids.my_progress_bar.value = 0.20
            self.ids.my_label.value = 1
            self.ids.my_label.text = f'Vraag {self.ids.my_label.value} / 5'


    def lichtAanzetten(self, nummerNFCreader):
        if nummerNFCreader == 0:
            GPIO.output(led_mn, GPIO.HIGH)
        elif nummerNFCreader == 1:
            GPIO.output(led_sn, GPIO.HIGH)
        elif nummerNFCreader == 2:
            GPIO.output(led_ts, GPIO.HIGH)
        elif nummerNFCreader == 3:
            GPIO.output(led_jm, GPIO.HIGH)
        elif nummerNFCreader == 4:
            GPIO.output(led_sc, GPIO.HIGH)
        elif nummerNFCreader == 5:
            GPIO.output(led_rs, GPIO.HIGH)


    #checkt of er een error is, als er meer dan 2 voorwerpen zijn opgetild
    def checkErr(self):
        if voorwerpPlaatsen.count(0) > 1:
            #checkt of een popup momenteel open is, zo ja, doet het dicht
            if isinstance(App.get_running_app().root_window.children[0], Popup):
                App.get_running_app().root_window.children[0].dismiss()
            #maakt de layout van de pop
            popupLayout = ErrorPopUp()
            layout = GridLayout(cols= 3, size_hint=(0.6, 0.7))
            #voegt de achtergrond toe aan de popup
            with layout.canvas.before:
                Color(0, 1,  0, 0.25)
                Rectangle(size=(layout.size))


            #self.popup = ModalView(size_hint=(None, None))
            with popupLayout.backgrounderror.canvas.before:
                Color(0.1,0.1,0.1, 1)
                Rectangle(pos=(self.center_x / 2, self.center_y / 2), size=(self.size[0] / 2, self.size[1] / 2))
            popupLayout.backgrounderror.size = self.size[0] / 2, self.size[1] / 2
            popupLayout.backgrounderror.pos = self.center_x / 2, self.center_y / 2
            popupLayout.ids.tafel.padding = [(self.size[0] / 13),0,0,0]

            #loopt door alle voorwerpen heen. Als een vorwerp is opgetild rood cirkel anders groen
            for rows in range(len(voorwerpPlaatsen)):
                if voorwerpPlaatsen[rows] == 0:
                    #rode cirkel maken met juiste afmeting & naam
                    red = RedCircle()
                    red.ids.circle_box.size = (self.size[0] / 2) / 3, self.size[1] / 2
                    red.ids.circle_title.text = voorwerpNamen[rows]
                    popupLayout.ids.tafel.add_widget(red)
                else:
                    #groene cirkel maken met juiste afmeting & naam
                    green = GreenCircle()
                    green.ids.circle_box.size = (self.size[0] / 2) / 3, self.size[1] / 2
                    green.ids.circle_title.text = voorwerpNamen[rows]
                    popupLayout.ids.tafel.add_widget(green)

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
        #self.lichtAanzetten(nummerNFCreader)

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
            if nummerNFCreader == 4:
                self.ids.info_scherm.add_widget(InfoSunCentered())
            if nummerNFCreader == 5:
                self.ids.info_scherm.add_widget(InfoRings())

    #functie die checkt wat voor antwoord bericht er van de arduino wordt verstuurd
    def antwoordBerichtChecken(self, message):
        print(message)
        #a_none
        if "none" in message:
            #TODO Antwoord weghalen van veld
            #GPIO.output(led_antwoord_goed, GPIO.LOW)
            #GPIO.output(led_antwoord_fout, GPIO.LOW)
            self.reset_timer()
            print("voorwerp opgetilt")
        else:
            vraag_index = questions.index(self.vragen[0])
            if antwoordeVragen[vraag_index] in message:
                #GPIO.output(led_antwoord_goed, GPIO.HIGH)
                self.reset_timer.cancel()
                self.next_question()
            else:
                #GPIO.output(led_antwoord_fout, GPIO.HIGH)
                print("TODO: fout")


    def closeRestartPopup(self, dt):
        self.restartScreen.dismiss()
        #restart vragen
        self.vragen = self.tienrandom()
        self.ids.my_label_question.text = self.vragen[0]
        self.ids.my_progress_bar.value = 0.20
        self.ids.my_label.value = 1
        self.ids.my_label.text = f'Vraag {self.ids.my_label.value} / 5'

    #checkt het bericht dat de machine krijgt van de Arduino
    def arduinoCheck(self, message):
        #als het met een a begint, dan gaat het om de antwoord reader
        if(message[0] == 'a'):
            self.antwoordBerichtChecken(message)
        elif(message == "reset"):
            #restart popup
            self.restartScreen = ModalView(size_hint=(None, None))
            self.restartScreen.add_widget(self.createRestartPopup())
            self.restartScreen.open()
            #automisch de popup weghalen na 5 seconden
            Clock.schedule_once(self.closeRestartPopup, 3)
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
                        #GPIO.output(led_mn, GPIO.LOW)
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 1:
                    if "sn" in message:
                        #GPIO.output(led_sn, GPIO.LOW)
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 2:
                    if "ts" in message:
                        #GPIO.output(led_ts, GPIO.LOW)
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 3:
                    if "jm" in message:
                        #GPIO.output(led_jm, GPIO.LOW)
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 4:
                    if "sc" in message:
                        #GPIO.output(led_sc, GPIO.LOW)
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
                elif numberReader == 5:
                    if "rs" in message:
                        #GPIO.output(led_rs, GPIO.LOW)
                        voorwerpPlaatsen[numberReader] = 1
                        self.terugzettenErrorCheck()
                    else:
                        print("error")
            except Exception as e:
                print("verkeerde input")
                print(e)


    #als een voorwerp terug gezet wordt, check of er nog één voorwerp vast wordt gehouden, zoja, geef info weer
    def terugzettenErrorCheck(self):
        if voorwerpPlaatsen.count(0) == 1:
            self.popup.dismiss()
            self.ids.info_scherm.clear_widgets()
            #loopt door de voorwerpen array heen en laat de informatie zien van één voorwerp dat opgetilt is
            for nfcreader in range(len(voorwerpPlaatsen)):
                if voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 0:
                    #self.ids.info_scherm.clear_widgets()
                    self.ids.info_scherm.add_widget(InfoMoon())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 1:
                    #self.ids.info_scherm.clear_widgets()
                    self.ids.info_scherm.add_widget(InfoSaturnMoon())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 2:
                    self.ids.info_scherm.add_widget(InfoTelescoop())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 3:
                    self.ids.info_scherm.add_widget(InfoJupiter())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 4:
                    self.ids.info_scherm.add_widget(InfoSunCentered())
                elif voorwerpPlaatsen[nfcreader] == 0 and nfcreader == 5:
                    self.ids.info_scherm.add_widget(InfoRings())
        elif voorwerpPlaatsen.count(0) == 0:
            self.popup.dismiss()
            self.ids.info_scherm.clear_widgets()
            # Instructie widget maken en de afmetingen meegeven
            instructions = Instruction()
            instructions.ids.intro.size = (self.size[0] * 0.9, self.height * 0.5)
            instructions.ids.intro.padding = (self.size[0] * 0.1, 50, 0, 0)
            self.ids.info_scherm.add_widget(instructions)
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
  #ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
  ser.reset_input_buffer()
  MyApp().run()
