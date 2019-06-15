from SideScroller.Objects.ObjectBase import ObjectBase
import SideScroller.utils as utils
import pygame


class Cube(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        ObjectBase.__init__(self, screen, args, parent)
        self.full_w = utils.get_mandatory(args, "@w", int)
        self.full_h = utils.get_mandatory(args, "@h", int)
        self.w = self.full_w
        self.h = self.full_h
        self.z = 0

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 2)

    # def update(self, pressed_keys):
    #     self.z += 1
    #
    #     self.w = self.full_w / self.z
    #     self.h = self.full_h / self.z