import typing

import pygame

from SideScroller.Misc.Ticker import Ticker
from SideScroller.utils import get_mandatory, rect_a_touch_b, scale_coords
from SideScroller.DisplayMethods.Color import Color, DisplayBase
from SideScroller.Globals.GlobalVariable import get_sys_var


class ObjectBase:
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        self.screen = screen
        self.args = args
        self.parent = parent

        self.x = get_mandatory(args, "@x", int)
        self.y = get_mandatory(args, "@y", int)

        self.x, self.y = scale_coords((self.x, self.y))

        self.screen_w, self.screen_h = self.screen.get_size()

        self.display = Color(screen, (255, 0, 255), 10, 10)
        self.w, self.h = self.display.get_size()

        self.on_screen_cache = True
        self.on_mouse_over_cache = False
        self.deleted = False

        self.ticker = Ticker()
        self.time_delta = self.ticker.tick

        self.states = {}
        self.state = None

        self.x_delta = 0
        self.y_delta = 0

        self.debug_color = get_sys_var("debug-color")

        self.oncreate()

    def set_display_method(self, method:'DisplayBase'):
        self.display = method
        self.w, self.h = self.display.get_size()

    @property
    def is_onscreen(self):
        return rect_a_touch_b(self.rect, (0, 0, self.screen_w, self.screen_h))

    @property
    def rect(self):
        return self.x, self.y, self.w, self.h

    def system_onroomenter(self):
        """DONT OVERRRIDE ME!!!!!!!!!!!"""
        self.ticker = Ticker()

    def system_update(self):
        self.time_delta = self.ticker.tick

    def move(self, x, y, fire_onscreen_event=True):
        self.x += x
        self.y -= y
        self.x_delta = x
        self.y_delta = y
        onscreen = self.is_onscreen
        if fire_onscreen_event:
            if onscreen != self.on_screen_cache:
                if onscreen:
                    self.onscreenenter()
                else:
                    self.onscreenleave()
                self.on_screen_cache = onscreen
            self.onmove(x, y)
            self.collision_detecion(self.parent.props.array)

        return onscreen

    def collision_detecion(self, objects: typing.List['ObjectBase']):
        for obj in objects:
            if rect_a_touch_b(self.rect, obj.rect):
                self.oncollide(obj)
                obj.oncollide(self)

    def time_move(self, x_velocity:float, y_velocity:float):
        self.move(x_velocity * self.time_delta, y_velocity * self.time_delta)

    def undo_last_move(self):
        self.move(-self.x_delta, -self.y_delta, fire_onscreen_event=False)

    def delete(self):
        self.ondelete()
        self.deleted = True

    def change_room(self, new_room):
        self.parent.parent.set_room(new_room)

    def update(self, pressed_keys):
        pass

    def draw(self):
        pass

    def onclick(self, button, pos):
        pass

    def onrelease(self, button, pos):
        pass

    def onmousedown(self, button, pos):
        pass

    def onmouseup(self, button, pos):
        pass

    def onmousemotion(self, position, relative, buttons):
        pass

    def onmouseover(self, position, relative, buttons):
        pass

    def onmouseleave(self, position, relative, buttons):
        pass

    def onkeydown(self, unicode, key, modifer, scancode):
        pass

    def onkeyup(self, key, modifier, scancode):
        pass

    def onroomenter(self):
        pass

    def onroomleave(self, next_room):
        pass

    def onquit(self):
        pass

    def ondelete(self):
        pass

    def oncreate(self):
        pass

    def onevent(self, event):
        pass

    def onscreenenter(self):
        pass

    def onscreenleave(self):
        pass

    def onmove(self, x_change, y_change):
        pass

    def oncollide(self, obj:'ObjectBase'):
        pass
