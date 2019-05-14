import pygame
from SideScroller.DisplayMethods.DisplayBase import DisplayBase
from SideScroller.Globals.Cache import get_image


class Image(DisplayBase):
    def __init__(self, screen: pygame.Surface, image:str):
        DisplayBase.__init__(self)
        self.image = get_image(image)
        self.w, self.h = self.image.get_size()
        self.screen = screen

    def draw(self, x, y):
        self.screen.blit(self.image, (x, y))
