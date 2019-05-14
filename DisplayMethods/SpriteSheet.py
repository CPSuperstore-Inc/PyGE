import pygame
from SideScroller.DisplayMethods.DisplayBase import DisplayBase
from SideScroller.Globals.Cache import get_spritesheet


class SpriteSheet(DisplayBase):
    def __init__(self, screen: pygame.Surface, spritesheet:str):
        DisplayBase.__init__(self)
        self.spritesheet = get_spritesheet(spritesheet)
        self.screen = screen
        self.w, self.h = self.spritesheet.current_image.get_size()

    def draw(self, x, y):
        self.screen.blit(self.spritesheet.current_image, (x, y))
