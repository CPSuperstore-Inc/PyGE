import typing

import pygame

from SideScroller.Screens.ScreenBase import ScreenBase
from SideScroller.ASQL import ASQL
from SideScroller.utils import get_mandatory, point_in_rect
from SideScroller.Objects.ObjectBase import ObjectBase
from SideScroller.utils import rect_a_touch_b
from SideScroller.Globals.GlobalVariable import get_sys_var
from SideScroller.Errors import ObjectNotDeclaredException

HALL = 0


class Room(ScreenBase):
    def __init__(self, screen, data:dict, custom_objects:typing.List, parent):
        ScreenBase.__init__(self, screen)
        self.name = get_mandatory(data, "@name")
        self.props = ASQL()
        self.custom_objects = custom_objects
        self.parent = parent

        for item in data:
            if type(data[item]) is list:
                for count in range(len(data[item])):
                    if not item.startswith("@"):
                        found = False
                        for c in self.custom_objects:
                            if c.__name__ == item:
                                self.props.append(c(self.screen, data[item][count], self))
                                found = True
                                break
                        if found is False:
                            raise ObjectNotDeclaredException("The Object '{0}' Is Referenced In The XML, But Is Not Declared. Please Place A Reference To The '{0}' Class In The 'custom_objects' List When Calling The 'side_scroller' Function.".format(item))
            else:
                if not item.startswith("@"):
                    found = False
                    for c in self.custom_objects:
                        if c.__name__ == item:
                            if data[item] is None:
                                data[item] = {}
                            self.props.append(c(self.screen, data[item], self))
                            found = True
                            break
                    if found is False:
                        raise ObjectNotDeclaredException(
                            "The Object '{0}' Is Referenced In The XML, But Is Not Declared. Please Place A Reference To The '{0}' Class In The 'custom_objects' List When Calling The 'side_scroller' Function.".format(
                                item))


    def enter_room(self):
        for prop in self.props.array:
            prop.system_onroomenter()
            prop.onroomenter()

    def leave_room(self, new_room):
        for prop in self.props.array:
            prop.onroomleave(new_room)


    def quit_action(self):
        can_quit = True
        for prop in self.props.array:
            if prop.onquit() is False:
                can_quit = False
        return can_quit

    def draw(self):
        for prop in self.props.array:
            if prop.on_screen_cache:
                prop.draw()
            if get_sys_var("debug"):
                pygame.draw.rect(self.screen, prop.debug_color, prop.rect, 3)

    def update(self, events:list):
        for prop in self.props.array:
            if prop.deleted:
                self.props.array.remove(prop)
                continue
            prop.system_update()
            prop.update(pygame.key.get_pressed())
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if point_in_rect(event.pos, prop.rect):
                        prop.onclick(event.pos, event.button)
                    prop.onmousedown(event.pos, event.button)
                if event.type == pygame.MOUSEBUTTONUP:
                    if point_in_rect(event.pos, prop.rect):
                        prop.onrelease(event.pos, event.button)
                    prop.onmouseup(event.pos, event.button)
                if event.type == pygame.MOUSEMOTION:
                    prop.onmousemotion(event.pos, event.rel, event.buttons)
                    if point_in_rect(event.pos, prop.rect):
                        if prop.on_mouse_over_cache is False:
                            prop.on_mouse_over_cache = True
                            prop.onmouseover(event.pos, event.rel, event.buttons)
                    else:
                        if prop.on_mouse_over_cache:
                            prop.on_mouse_over_cache = False
                            prop.onmouseleave(event.pos, event.rel, event.buttons)
                if event.type == pygame.KEYDOWN:
                    prop.onkeydown(event.unicode, event.key, event.mod, event.scancode)
                if event.type == pygame.KEYUP:
                    prop.onkeyup(event.key, event.mod, event.scancode)
                prop.onevent(event)

    def move_many(self, objects: typing.List['ObjectBase'], x, y, fire_onscreen_event:bool=True, static: typing.List['ObjectBase']=None, check_collision:bool=False):
        if static is None:
            static = self.props

        abort = False
        for p in objects:
            p.move(x, y, fire_onscreen_event)
            for s in static:
                if rect_a_touch_b(p.rect, s.rect):
                    abort = True

        if abort:
            for p in objects:
                p.undo_last_move()
