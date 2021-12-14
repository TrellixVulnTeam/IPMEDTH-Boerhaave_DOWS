import random

def tienrandom():
  questions = ['vraag1', 'vraag2', 'vraag3', 'vraag4', 'vraag5', 'vraag6', 'vraag7', 'vraag8', 'vraag9', 'vraag10']
  randomvragen = []
  randomlist = random.sample(range(0, 10), 10)
  print(randomlist)
  for item in randomlist:
    randomvragen.append(questions[item])
    
  print(randomvragen)
if __name__ == '__main__':
  tienrandom()