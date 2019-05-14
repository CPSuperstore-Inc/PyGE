import pygame
from SideScroller.DisplayMethods.DisplayBase import DisplayBase


class Color(DisplayBase):
    def __init__(self, screen: pygame.Surface, color:tuple, width:int, height:int):
        DisplayBase.__init__(self)
        self.color = color
        self.screen = screen
        self.w, self.h = width, height

    def draw(self, x ,y):
        pygame.draw.rect(self.screen, self.color, (x, y, self.w, self.h))
