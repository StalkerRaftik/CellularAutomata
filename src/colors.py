import random

WHITE = 255, 255, 255
BLACK = 0, 0, 0
AZURE = 0, 127, 255
ORANGE = 255, 165, 0


def RANDOM():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def RANDOM_NEAR(color):
    new_color = []
    for base_clr in color:
        new_base_clr = min(max(0, base_clr + random.randint(-50, 50)), 255)
        new_color.append(new_base_clr)

    return new_color
