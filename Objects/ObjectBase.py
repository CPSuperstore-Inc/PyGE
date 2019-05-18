import typing

import pygame
import matplotlib.path as mpl_path
import numpy as np

from SideScroller.Misc.Ticker import Ticker
from SideScroller.utils import get_mandatory, rect_a_touch_b, scale_coords, get_optional
from SideScroller.DisplayMethods.Color import Color, DisplayBase
from SideScroller.Globals.GlobalVariable import get_sys_var


class ObjectBase:
    def __init__(self, screen:pygame.Surface, args: dict, parent):
        """
        This is the object ALL objects MUST inherit from to be used in a room.
        This is the parent of ALL objects.
        :param screen: The screen to draw the object to
        :param args: The dictionary of properties specified in the XML. NOTE: Any property defined in a tag, will have the '@' infront of it 
        :param parent: The room the object will live in 
        """
        self.screen = screen
        self.args = args
        self.parent = parent

        self.x = get_mandatory(args, "@x", int)
        self.y = get_mandatory(args, "@y", int)

        self.locked = get_optional(args, "@locked", "false")

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

        self.model_type = type(self).__name__

        self.debug_color = get_sys_var("debug-color")

        self.oncreate()

    def set_display_method(self, method:'DisplayBase'):
        """
        Sets the display method of the object
        :param method: The display method
        """
        self.display = method
        self.w, self.h = self.display.get_size()

    @property
    def is_onscreen(self):
        """
        Returns if this object is in any way touching the screen
        """
        return rect_a_touch_b(self.rect, (0, 0, self.screen_w, self.screen_h))

    @property
    def rect(self):
        """
        Returns the rect representation of the object in the format (x, y, width, height)
        """
        return self.x, self.y, self.w, self.h

    @property
    def point_array(self):
        """
        Returns this object as a point array in the format [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        """
        return (self.x, self.y), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), (self.x + self.w, self.y)

    @property
    def polygon(self):
        """
        Returns a polygon representaion of the object (As a MatPlotLib Path object)
        :return: 
        """
        return mpl_path.Path(np.array(self.point_array))

    def system_onroomenter(self):
        self.ticker = Ticker()

    def system_update(self):
        self.time_delta = self.ticker.tick

    def move(self, x, y, fire_onscreen_event=True):
        """
        This is the foundation for how this object is able to move
        Note: The object CAN NOT move if the "locked" property is set to True
        :param x: the x position change (in pixels)
        :param y: the y position change (in pixels)
        :param fire_onscreen_event: If the "onmove" event will be fired after movingf the object
        """
        if self.locked == "true":
            return True
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
        """
        Checks collision between this object, and a list of other objects.
        If collision is detected, the "oncollide" event of both objects is run
        :param objects: The list of objects to check
        """
        for obj in objects:
            if rect_a_touch_b(self.rect, obj.rect):
                self.oncollide(obj)
                obj.oncollide(self)

    def is_touching(self, other:'ObjectBase'):
        """
        Determines if this object is touching another object
        NOTE: Will NOT fire the "oncollide" event
        :param other: The object to check against
        :return: If the objects are touching
        """
        me = self.polygon
        you = other.point_array

        for p in you:
            if me.contains_point(p):
                return True
        return False

    def time_move(self, x_velocity:float, y_velocity:float):
        """
        Moves the object based on time (not framerate)
        This is the funtion which should be used for all object movement
        :param x_velocity: the velocity (speed) in the x direction
        :param y_velocity: the velocity (speed) in the y direction
        """
        self.move(x_velocity * self.time_delta, y_velocity * self.time_delta)

    def undo_last_move(self):
        """
        Undoes the object's last movement
        This DOES NOT fire the "onmove" event
        """
        self.move(-self.x_delta, -self.y_delta, fire_onscreen_event=False)

    def delete(self):
        """
        Deletes this object from memory
        This also fires the "ondelete" event
        """
        self.ondelete()
        self.deleted = True

    def change_room(self, new_room):
        """
        Changes the current room to a different one
        This fires the "onroomleave" event for all objects in this room, and "onroomenter" for the objects in the new room
        :param new_room: The room to move to
        """
        self.parent.parent.set_room(new_room)

    def is_touching_type(self, model:str):
        """
        Checks if this object is touching another object of a specified type (from a specified Class)
        NOTE: Will NOT fire the "oncollide" event
        :param model: The name of the type/class to check against
        :return: If there is colloision
        """
        for obj in self.parent.props.array:
            if obj.model_type == model:
                if rect_a_touch_b(self.rect, obj.rect):
                    return True
        return False

    def get_all_type(self, model:str):
        """
        Gets all of the objets of a specified class/type
        :param model: The class/type to select from
        :return: A list of matches
        """
        matches = []
        for obj in self.parent.props.array:
            if obj.model_type == model:
                matches.append(obj)
        return matches

    def highlight_point(self, point, y=None, color=(255, 255, 255), radius=3):
        """
        Highlights a specified point (if run in the object's "draw" method) with a circle
        :param point: The point to highlight in the format (x, y), or the x position of the point
        :param y: If the "point" parameter contains the 'x' position, this MUST contain the y position
        :param color: The color to draw the circle as
        :param radius: The radius of the circle
        """
        if y is None:
            x, y = point
        else:
            x = point
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)

    def draw_alpha(self, source, opacity, pos=None):
        """
        Draws the pygame Surface with transparency
        :param source: the pygame Surface
        :param opacity: the opacity of the object (0 = invisible, 255 = visible)
        :param pos: the location to draw the object at (levae blank for the location of this object)
        """
        if pos is None:
            x, y = (self.x, self.y)
        else:
            x, y = pos
        # noinspection PyArgumentList
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(self.screen, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        self.screen.blit(temp, (x, y))

    def update(self, pressed_keys):
        """
        Overridable method run once per frame. This is for all of the logic the object requires
        DO NOT do any drawing here. It will NOT get displayed
        :param pressed_keys: The list of the states of each key. Indexes are based on ASCII values. Ex. 101=e, so pressed_keys[101] = state of the 'e' key
        """
        pass

    def draw(self):
        """
        Overridable method run once per frame. This is for all of the drawing which needs to be done.
        It is stronlgy recomended to keep all of your logic in the "update" method, and your visual updates here.
        NOTE: this method WILL NOT run if the object is off the screen
        """
        pass

    def onclick(self, button, pos):
        """
        Overridable event run each time this object is clicked (the mouse changes to the down state)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        :return: 
        """
        pass

    def onrelease(self, button, pos):
        """
        Overridable event run each time this object is released (the mouse changes to the up state)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        """
        pass

    def onmousedown(self, button, pos):
        """
        Overridable event run each time the mouse changes to the down state (regardless if it is over this object)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor 
        """
        pass

    def onmouseup(self, button, pos):
        """
        Overridable event run each time the mouse changes to the down state (regardless if it is over this object)
        :param button: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        :param pos: The position of the mouse cursor
        """
        pass

    def onmousemotion(self, position, relative, buttons):
        """
        Overridable event run each time the mouse moves
        :param position: The position of the mouse cursor on the screen
        :param relative: The amount of distance the mouse has moved since the last method call
        :param buttons: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        """
        pass

    def onmouseover(self, position, relative, buttons):
        """
        Overridable event run each time the mouse moves on top of this object
        :param position: The position of the mouse cursor on the screen
        :param relative: The amount of distance the mouse has moved since the last method call
        :param buttons: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        """
        pass

    def onmouseleave(self, position, relative, buttons):
        """
        Overridable event run each time the mouse moves off of this object
        :param position: The position of the mouse cursor on the screen
        :param relative: The amount of distance the mouse has moved since the last method call
        :param buttons: A tuple of the states of the mouse in the format (left_mouse, middle_mouse/mouse_wheel, right_mouse)
        """
        pass

    def onkeydown(self, unicode, key, modifier, scancode):
        """
        Overridable event run each time any key on the keyboard is changed to the down state
        :param unicode: The character version of the key pressed (affected by keyboard modifiers)
        :param key: the character code of the key presed (ex. e=101)
        :param modifier: a bitmask representation of the keyboard modifiers used. Use "SideScroller.utils.deconstruct_modifier_bitmask" to convert to a list of modifiers
        :param scancode: The platform-specific key code (WARNING: Can be different between different keyboards)
        """
        pass

    def onkeyup(self, key, modifier, scancode):
        """
        Overridable event run each time any key on the keyboard is changed to the up state 
        :param key: the character code of the key presed (ex. e=101)
        :param modifier: a bitmask representation of the keyboard modifiers used. Use "SideScroller.utils.deconstruct_modifier_bitmask" to convert to a list of modifiers
        :param scancode: The platform-specific key code (WARNING: Can be different between different keyboards)
        :return: 
        """
        pass

    def onroomenter(self):
        """
        Overridable event run each time the user enters the room which contains this object
        """
        pass

    def onroomleave(self, next_room):
        """
        Overridable event run each time the user leaves the room which contains this object
        :param next_room: The name of the room the user is moving to
        """
        pass

    def onquit(self):
        """
        Overridable event run when the game is quit (closed)
        """
        pass

    def ondelete(self):
        """
        Overridable event run when this object is deleted from memory
        """
        pass

    def oncreate(self):
        """
        Overridable event run when this object is created
        """
        pass

    def onevent(self, event):
        """
        Overridable event run each time ANY pygame event takes place
        :param event: The pygame event object
        """
        pass

    def onscreenenter(self):
        """
        Overridable event run each time the object moves from being off the screen to back on the screen
        """
        pass

    def onscreenleave(self):
        """
        Overridable event run each time the object moves from being on the screen to off the screen
        """
        pass

    def onmove(self, x_change, y_change):
        """
        Overridable event run each time this object is moved
        :param x_change: the change in the x direction the object has moved
        :param y_change: the change in the y direction the object has moved
        """
        pass

    def oncollide(self, obj:'ObjectBase'):
        """
        Overridable event run each time this object collides with another
        :param obj: the object which this object has collided with
        """
        pass
