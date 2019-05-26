import pygame

from SideScroller.Objects.ObjectBase import ObjectBase
from SideScroller.DisplayMethods.Color import Color
from SideScroller.Screens.Room import Room
from SideScroller.Globals.GlobalVariable import get_var
from SideScroller.utils import convert_color


class Wall(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        height = get_var("floor-height")
        args["@x"] = 0
        args["@y"] = 0
        ObjectBase.__init__(self, screen, args, parent)
        self.set_display_method(Color(screen, convert_color(args["@color"]), screen.get_width(), screen.get_height() - height))

    def draw(self):
        self.display.draw(self.x, self.y)

    @property
    def metadata(self):
        return {
            "color": self.display.color
        }