import pygame

from SideScroller.Objects.ObjectBase import ObjectBase
from SideScroller.DisplayMethods.Color import Color
from SideScroller.Screens.Room import Room
from SideScroller.Globals.GlobalVariable import get_var


class Floor(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        height = get_var("floor-height")
        args["@x"] = 0
        args["@y"] = screen.get_height() - height
        ObjectBase.__init__(self, screen, args, parent)
        self.set_display_method(Color(screen, eval(args["@color"]), screen.get_width(), height))

    def draw(self):
        self.display.draw(self.x, self.y)
