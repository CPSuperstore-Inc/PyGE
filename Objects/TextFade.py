import pygame

from SideScroller.Objects.ObjectBase import ObjectBase
from SideScroller.Misc.Function import Function
from SideScroller.Screens.Room import Room
from SideScroller.utils import get_optional, get_mandatory


class TextFade(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):

        self.font_object = None         # type: pygame.font.Font
        self.text_object = None         # type: pygame.Surface
        self.fade_function = None       # type: Function
        self.fade_speed = 0

        self.font = get_mandatory(args, "@font", str)
        self.size = get_mandatory(args, "@size", int)

        self.alpha = get_optional(args, "@alpha", 255, int)

        self.color = eval(get_mandatory(args, "@color", str))
        self.antialiasing = bool(get_optional(args, "@antialiasing", 1, int))
        self.text = get_optional(args, "@text", "", str)

        self.generate_font()
        self.generate_text()

        ObjectBase.__init__(self, screen, args, parent)

    def generate_font(self):
        self.font_object = pygame.font.Font(self.font, self.size)

    def generate_text(self):
        self.text_object = self.font_object.render(self.text, self.antialiasing, self.color)

    # region Setters
    def set_font(self, font:str):
        self.font = font
        self.generate_font()

    def set_size(self, size:int):
        self.size = size
        self.generate_font()

    def set_text(self, text:str):
        self.text = text
        self.generate_text()

    def set_antialiasing(self, antialiasing:bool):
        self.antialiasing = antialiasing
        self.generate_text()

    def set_color(self, color:tuple):
        self.color = color
        self.generate_text()
    # endregion

    def fade_in(self, duration:float=None, alpha_per_s:float=None):
        self.alpha = 0
        if duration is not None:
            self.fade_speed = 255 / duration
        elif alpha_per_s is not None:
            self.fade_speed = alpha_per_s
        else:
            raise ValueError("Please Define Either The 'duration' Or The 'alpha_per_s'")

    def fade_out(self, duration:float=None, alpha_per_s:float=None):
        self.fade_in(duration, alpha_per_s)
        self.alpha = 255
        self.fade_speed *= -1

    def draw(self):
        if self.fade_speed != 0:
            change = self.time_delta * self.fade_speed
            self.alpha += change
            if self.alpha > 255 or self.alpha < 0:
                fade_in = self.fade_speed > 0
                self.fade_speed = 0
                self.onfadecomplete(fade_in)
        self.draw_alpha(self.text_object, self.alpha)

    def onfadecomplete(self, fade_in:bool):
        pass