"""An old-skool scrolling game for the BBC microbit.
You are in a spaceship decending to the surface of an unknown a planet. Use the buttons to manoeuvre left and
right to avoid the accumulated space junk that is suspended in orbit around he planet.
Your spaceship is the bright dot on the top line of the display. The the less bright dots are the space junk."""

from microbit import *
import random


# Some constants
SCREEN_WIDTH = 5
SCREEN_HEIGHT = 5
SECONDS_PER_STEP = 1
POLLS_PER_SECOND = 10
SCENERY_LENGTH_IN_SCREENS = 5 # Tune this down to fit in RAM
NUM_OBSTACLES = 100


def make_obstacles(width, height, num):
    obstacles = set()
    possible_locations = set()
    for x in range(width):
        for y in range(3, height):
            possible_locations.add((x, y))
    
    for i in range(num):
        if not possible_locations:
            break
        
        x, y = random.choice(list(possible_locations))
        obstacles.add((x,y))
        
        possible_locations.remove((x, y))
        
        possible_locations.discard((x-1, y))
        possible_locations.discard((x-1, y-1))
        possible_locations.discard((x-1, y+1))
        possible_locations.discard((x, y-1))
        possible_locations.discard((x, y+1))
        possible_locations.discard((x+1, y))
        possible_locations.discard((x+1, y-1))
        possible_locations.discard((x+1, y+1))
    
    return obstacles


def make_scenery(width, height, num_obstacles):
    obstacles = make_obstacles(width, height, num_obstacles)
    
    scenery = Image(width, height)
    for x, y in obstacles:
        scenery.set_pixel(x, y, 4)
    
    return scenery
    

def move_ship(ship_x, ship_y):
    if button_a.is_pressed() and button_b.is_pressed():
        return ship_x, ship_y
    elif button_a.is_pressed():
        return max(0, ship_x - 1), ship_y
    elif button_b.is_pressed():
        return min(4, ship_x + 1), ship_y
    else:
        return ship_x, ship_y
        

def detect_collision(scenery, ship_x, ship_y):
    return scenery.get_pixel(ship_x, ship_y) > 0
    
    
def draw_screen(scenery, ship_x, ship_y):
    scene = scenery.crop(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).copy()
    scene.set_pixel(ship_x, ship_y, 9)
    display.show(scene)
    

def scroll_up(scenery):
    row_zero = [scenery.get_pixel(x, 0) for x in range(scenery.width())]
    scenery = scenery.shift_up(1)
    for x, v in enumerate(row_zero):
        scenery.set_pixel(x, scenery.height()-1, v)
    return scenery


while True:
    scenery = make_scenery(SCREEN_WIDTH,
                           SCREEN_HEIGHT * SCENERY_LENGTH_IN_SCREENS,
                           NUM_OBSTACLES)
    
    ship_x = SCREEN_WIDTH // 2
    ship_y = 0
    collision = False
    
    while not collision:
        scenery= scroll_up(scenery)
        collision = detect_collision(scenery, ship_x, ship_y)
    
        if collision:
            break

        for _ in range(SECONDS_PER_STEP * POLLS_PER_SECOND):
            ship_x, ship_y = move_ship(ship_x, ship_y)

            collision = detect_collision(scenery, ship_x, ship_y)
            if collision:
                break
            
            draw_screen(scenery, ship_x, ship_y)
            sleep(1000 / POLLS_PER_SECOND)
    
    display.show(Image.SKULL)
    sleep(2000)
