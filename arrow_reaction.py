# Add your Python code here. E.g.
from microbit import *

import random


class ArrowReactionGame(object):

    options = ['W', 'E']
    delay_decrease = 0.9

    def __init__(self):
        self.total_score = 0
        self.current_delay = 1000

    def play_game(self):
        self.current_delay = 1000
        display.scroll('READY')
        sleep(1000)
        while True:
            random_choice = random.choice(self.options)
            if random_choice == 'W':
                display.show(Image.ARROW_W)
            elif random_choice == 'E':
                display.show(Image.ARROW_E)
            current_time = running_time()
            while current_time + self.current_delay > running_time():
                if button_a.was_pressed():
                    if random_choice == 'W':
                        self.total_score += 1
                        break
                    else:
                        self.game_over()
                if button_b.was_pressed():
                    if random_choice == 'E':
                        self.total_score += 1
                        break
                    else:
                        self.game_over()
                sleep(1)
            else:
                self.game_over()
            display.show(Image(5, 5))
            sleep(self.current_delay)
            self.current_delay *= self.delay_decrease

    def game_over(self):
        display.show(Image.SAD)
        sleep(1000)
        while True:
            display.scroll(str(self.total_score))
            sleep(1000)


game = ArrowReactionGame()
game.play_game()
