from game import Game
from threading import Event
import keyboard

stopFlag = Event()
game = Game(stopFlag)
game.start()

VALID_INPUTS = 'wasd'

while True:
    text = keyboard.read_key()#input("next move > ")
    if text == 'new':
        stopFlag.set()
        stopFlag = Event()
        game = Game(stopFlag)
        game.start()
    elif text in VALID_INPUTS:
        game.set_user_action(text)
