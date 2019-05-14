import pygame

import os

from sub_image import get_sub_image


def reload_preset_boards():
    for img in os.listdir("rescources/images/boards/preset"):
        preset_boards[img.replace(".png", "")] = pygame.transform.scale(pygame.image.load("rescources/images/boards/preset/{}".format(img)), (128, 64))

doors = {
    "suite": pygame.transform.scale(pygame.image.load("rescources/images/door/suite.png"), (64, 80)),
    "bedroom": pygame.transform.scale(pygame.image.load("rescources/images/door/bedroom.png"), (64, 80)),
    "glass": pygame.transform.scale(pygame.image.load("rescources/images/door/glass.png"), (64, 80)),
    "elevator": pygame.transform.scale(pygame.image.load("rescources/images/door/elevator.png"), (128, 128))
}

garbage = {
    "banana": pygame.transform.scale(pygame.image.load("rescources/images/garbage/banana.png"), (32, 32)),
}

props = {
    "green_bed": pygame.transform.scale(pygame.image.load("rescources/images/props/green_bed.png"), (114, 64)),
    "small_window": pygame.transform.scale(pygame.image.load("rescources/images/props/small_window.png"), (64, 64)),
    "wood_desk": pygame.transform.scale(pygame.image.load("rescources/images/props/wood_desk.png"), (100, 50)),
    "wood_chair_front": pygame.transform.scale(pygame.image.load("rescources/images/props/wood_chair_front.png"), (41, 59)),
    "wood_chair_back": pygame.transform.scale(pygame.image.load("rescources/images/props/wood_chair_back.png"), (41, 53)),
    "wood_dresser": pygame.transform.scale(pygame.image.load("rescources/images/props/wood_dresser.png"), (64, 96)),
    "fridge": pygame.transform.scale(pygame.image.load("rescources/images/props/fridge.png"), (45, 67)),
    "oven": pygame.transform.scale(pygame.image.load("rescources/images/props/oven.png"), (48, 53)),
    "microwave": pygame.transform.scale(pygame.image.load("rescources/images/props/microwave.png"), (48, 27)),
    "cupboard": pygame.transform.scale(pygame.image.load("rescources/images/props/cupboard.png"), (39, 48)),
    "sink": pygame.transform.scale(pygame.image.load("rescources/images/props/sink.png"), (39, 20)),
    "couch": pygame.transform.scale(pygame.image.load("rescources/images/props/couch.png"), (162, 66)),
    "front_desk": pygame.transform.scale(pygame.image.load("rescources/images/props/front_desk.png"), (98, 64)),
}

posters = {
    "goat": pygame.transform.scale(pygame.image.load("rescources/images/props/posters/goat.png"), (61, 91)),
    "dot": pygame.transform.scale(pygame.image.load("rescources/images/props/posters/dot.png"), (91, 61)),
    "welcome": pygame.transform.scale(pygame.image.load("rescources/images/props/posters/welcome.png"), (116, 61)),
}

computer = {
    "frame": pygame.transform.scale(pygame.image.load("rescources/images/computer/frame.png"), (800, 450)),
    "background": pygame.transform.scale(pygame.image.load("rescources/images/computer/background.png"), (800, 450)),
    "todo": pygame.transform.scale(pygame.image.load("rescources/images/computer/todo.png"), (32, 32)),
    "close": pygame.transform.scale(pygame.image.load("rescources/images/computer/close.png"), (16, 16)),
    "complete": pygame.transform.scale(pygame.image.load("rescources/images/computer/complete.png"), (32, 32)),
    "incomplete": pygame.transform.scale(pygame.image.load("rescources/images/computer/incomplete.png"), (32, 32)),
    "logout": pygame.transform.scale(pygame.image.load("rescources/images/computer/logout.png"), (25, 32)),
}

fire_full = pygame.transform.scale(pygame.image.load("rescources/images/damage/fire.png"), (112, 128))

fire = {}

cash = {
    "icon": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/cash/icon.png"), (32, 32)),
}

gwd = {
    "icon": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/gwd/icon.png"), (32, 32)),
    "player": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/gwd/player.png"), (22, 22)),
    "bad": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/gwd/bad.png"), (22, 22)),
    "spawner": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/gwd/spawner.png"), (32, 32))

}

paint = {
    "pencil": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/paint/pencil.png"), (32, 32)),
    "eraser": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/paint/eraser.png"), (32, 32)),
    "floppy": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/paint/floppy.png"), (32, 32)),
    "icon": pygame.transform.scale(pygame.image.load("rescources/images/computer/games/paint/icon.png"), (32, 32)),
}

interactive = {
    "monitor": pygame.transform.scale(pygame.image.load("rescources/images/interactive/monitor.png"), (64, 44)),
}

npc = {
    "bob": pygame.transform.scale(pygame.image.load("rescources/images/npc/bob.png"), (32, 96)),
    "sue": pygame.transform.scale(pygame.image.load("rescources/images/npc/sue.png"), (32, 96)),
    "larry": pygame.transform.scale(pygame.image.load("rescources/images/npc/larry.png"), (32, 96)),
}

front_desk = {
    "desk": pygame.transform.scale(pygame.image.load("rescources/images/front_desk/front_desk.png"), (800, 525)),
    "monitor": pygame.transform.scale(pygame.image.load("rescources/images/interactive/monitor.png"), (182, 125)),
    "clock": pygame.transform.scale(pygame.image.load("rescources/images/front_desk/clock.png"), (64, 32)),
}

preset_boards = {}
reload_preset_boards()



