"""
Example micro:bit application for the name badges at the 3rd Annual Man Global Systematic Investment Symposium

The app allows delegates to share their mood with each other by displaying emoji like images and make
important decisions by flipping a coin.

* The buttons cycle through the images
* Shaking the badge flips as coin and shows the outcome on the display.
* Press both buttons scrolls the name of the event on the screen

"""
from microbit import *
import random

answers = [
    "HEADS",
    "TAILS",
]

scroll_message = "MGSIS 2017"

all_images = [Image.HAPPY, Image.SAD, Image.CONFUSED,
              Image.ANGRY, Image.ASLEEP, Image.SURPRISED,
              Image.SILLY, Image.FABULOUS, Image.MEH,
              Image.HEART, Image.COW, Image.MUSIC_CROTCHET,
              Image.MUSIC_QUAVER, Image.MUSIC_QUAVERS,
              Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E,
              Image.ARROW_SE, Image.ARROW_S, Image.ARROW_SW,
              Image.ARROW_W, Image.ARROW_NW,
              Image.PITCHFORK, Image.XMAS, Image.PACMAN,
              Image.TARGET, Image.TSHIRT, Image.ROLLERSKATE,
              Image.HOUSE, Image.BUTTERFLY, Image.STICKFIGURE,
              Image.GHOST, Image.GIRAFFE, Image.SKULL, Image.UMBRELLA,
              Image.SNAKE, Image.YES, Image.NO]

num_images = len(all_images)

current_image = 0

try:
    with open('favourite.txt') as my_file:
        current_image = int(my_file.read())
except OSError:
    pass

while True:
    with open('favourite.txt', 'w') as my_file:
        my_file.write(str(current_image))
    display.show(all_images[current_image])
    sleep(200)
    while True:
        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll(scroll_message)
            break
        elif button_a.is_pressed():
            current_image = (num_images + current_image - 1) % num_images
            break
        elif button_b.is_pressed():
            current_image = (current_image + 1) % num_images
            break
        elif accelerometer.was_gesture("shake"):
            display.clear()
            sleep(800)
            display.scroll(random.choice(answers))
            break
