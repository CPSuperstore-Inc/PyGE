import pygame

from PyGE.DisplayMethods.DisplayBase import DisplayBase
from PyGE.Globals.Cache import get_image
from PyGE.utils import surface_center_rotate


class Image(DisplayBase):
    def __init__(self, screen: pygame.Surface, image:str, scale:float=1):
        """
        This class is to be used for all objects which are represented on the screen by an image
        :param screen: The surface to draw the image to
        :param image: The name of the image in the image cache. NOTE: The image MUST be stored in the cache
        :param scale: The factor to multiply the image size by (Ex: 2 doubles the size, and 0.5 halves the size)
        """
        DisplayBase.__init__(self)

        # get the image from the cache
        self.image = get_image(image)

        # calculate, and scale the image
        new_size = (int(self.image.get_width() * scale), int(self.image.get_height() * scale))
        self.image = pygame.transform.scale(self.image, new_size)

        self.offset = (0, 0)

        self.rotated = self.image

        # get the final size of the image
        self.w, self.h = self.image.get_size()

        # declare other properties
        self.screen = screen

    def rotate(self, radians):
        self.angle = radians
        self.rotated, self.offset = surface_center_rotate(self.image, radians)


    def draw(self, x, y):
        """
        Draws the image at the specified position
        :param x: The x position
        :param y: The y position
        """
        self.screen.blit(self.rotated, (x + self.offset[0], y + self.offset[1]))
