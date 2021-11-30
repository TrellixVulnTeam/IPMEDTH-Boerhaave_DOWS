from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('BasisSchermLayout.kv')

class MyLayout(Widget):
  def press_it(self):
    current = self.ids.my_progress_bar.value
    current_question = self.ids.my_label.value

    if current == 1:
      current = 0

    if current_question == 5:
      current_question = 0
    
    current += .20
    current_question += 1

    self.ids.my_progress_bar.value = current
    self.ids.my_label.value = current_question
    self.ids.my_label.text = f'Vraag {self.ids.my_label.value}'

class MyApp(App):
  def build(self):
    return MyLayout()

if __name__ == '__main__':
  MyApp().run()