import pygame

import os

from SideScroller.Misc.SpriteSheet import SpriteSheet
from SideScroller.utils import scale_image

# cache dictionaries
images = {}         # image cache
spritesheets = {}   # spritesheet cache
sounds = {}         # sound cache


def set_image(name, path, width=None, height=None):
    """
    Loads a single image into the image cache 
    :param name: The name to save the image in the cache as
    :param path: The path to the image save location
    :param width: The new width of the image
    :param height: The new height of the image
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("The File You Have Requested '{}' Could Not Be Located. Please Check The Path, And Ensure The File Exists.".format(path))
    img = pygame.image.load(path)
    if width is None:
        width = img.get_width()
    if height is None:
        height = img.get_height()
    images[name] = scale_image(pygame.transform.scale(img, (width, height)))


def get_image(name):
    """
    Gets the image from the cache by it's name
    :param name: The name of the image
    :return: The image from the cache
    """
    return images[name]


def cache_image_dir(dir_path:str, scale:float=1.0):
    """
    Loads every image from a directory into the cache.
    NOTE: The name of each image, is the image's file name without the extension
    NOTE: Will NOT check subdirectories.
    :param dir_path: The path to the directory of the files
    :param scale: The factor to multiply the image size by (Ex: 2 doubles the size, and 0.5 halves the size)
    """
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
    """
    Loads a spritesheet into the spritesheet cache
    :param name: The name to save the spritesheet under
    :param image: The path to the spritesheet
    :param w: The number of columns the spritesheet contains
    :param h: The number of rows the spritesheet contains
    :param duration: The length of time to stay on each frame
    :param final_size: The size to scale each frame to in the format (width, height)
    :param invisible_color: Some RGB color which will be ignored. (in general, select a color not in any of the images)
    """
    if not os.path.isfile(image):
        raise FileNotFoundError("The File You Have Requested '{}' Could Not Be Located. Please Check The Path, And Ensure The File Exists.".format(image))
    spritesheets[name] = SpriteSheet(image, w, h, duration, final_size, invisible_color)


def get_spritesheet(name):
    """
    Gets a spritesheet from the cache based on the name
    :param name: The name of the spritesheet
    :return: The spritesheet with the specified name
    """
    return spritesheets[name]


def set_sound(name:str, path:str, volume:float=1):
    """
    Loads a sound file into the cache based on the name
    :param name: The name to save the sound under
    :param path: The path of the sound
    :param volume: The volume to play the sound at (1 = Full, 0 = Mute)
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("The File You Have Requested '{}' Could Not Be Located. Please Check The Path, And Ensure The File Exists.".format(path))
    sounds[name] = pygame.mixer.Sound(path)
    sounds[name].set_volume(volume)


def get_sound(name):
    """
    Gets the sound from the cache based on the name
    :param name: The name of the sound
    :return: The sound with the specified name
    """
    return sounds[name]
