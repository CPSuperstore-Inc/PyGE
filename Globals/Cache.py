import pygame

import os

from SideScroller.Misc.SpriteSheet import SpriteSheet
from SideScroller.utils import scale_image

images = {}
spritesheets = {}


def set_image(name, path, width=None, height=None):
    img = pygame.image.load(path)
    if width is None:
        width = img.get_width()
    if height is None:
        height = img.get_height()
    images[name] = scale_image(pygame.transform.scale(img, (width, height)))


def get_image(name):
    return images[name]


def cache_image_dir(dir_path:str, scale:float=1.0):
    for name in os.listdir(dir_path):
        path = os.path.join(dir_path, name)
        if os.path.isdir(path):
            continue

        name = name[:name.index(".")]
        image = pygame.image.load(path)
        new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
        image = pygame.transform.scale(image, new_size)
        images[name] = image


def set_spritesheet(name, image:str, w:int, h:int, duration:float=None, final_size:tuple=None, invisible_color:tuple=(0, 0, 1)):
    spritesheets[name] = SpriteSheet(image, w, h, duration, final_size, invisible_color)


def get_spritesheet(name):
    return spritesheets[name]

