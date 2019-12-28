import typing

import pygame
import xmltodict
import json as js_to_the_o_to_the_n

from PyGE.Screens.Room import Room
from PyGE.Objects.ObjectBase import ObjectBase
from PyGE.Errors import RoomNotDeclaredException, InvalidXMLException
from PyGE.Globals.Objects import PREMADE_OBJECTS
from PyGE.DisplayMethods import DisplayBase


pygame.init()


class PyGE:
    def __init__(self, screen: pygame.Surface, level_data:str, starting_room: str, custom_objects:typing.List, load_mode:int=0, background_color:tuple=None):
        """
        This is the most important object in the entire system!
        You can use a custom version of this class by passing in a refrence to the class into the "alt_side_scroller" property
        in the function call which starts the engine. We recomend building a class which inherits from this one and overiding what you need to
        :param screen: the screen to draw the game to
        :param level_data: the XML representation of the level 
        :param starting_room: the name of the room to start the user in
        :param custom_objects: a list of the references to the custom objects which will be used (not including objects provided by the engine)
        :param load_mode: The mode ID of the method to interpret the level data as (0=XML, 1=JSON)
        :param background_color: The background color to use (tuple only) unless a room specifies otherwise
        """
        self.mouse_cursor = None            # type: DisplayBase
        self.load_mode = load_mode
        self.screen = screen
        self.level_data = level_data
        self.rooms = {}
        self.sub_rooms = {}
        self.custom_objects = PREMADE_OBJECTS + custom_objects
        self.background_color = background_color
        if self.background_color is None:
            self.background_color = (0, 0, 0)

        self.load_game()
        self.room = None

        self.set_room(starting_room)

    def load_game(self, level_data: str=None):
        modes = {
            0: self.load_from_xml,
            1: self.load_from_json
        }
        modes[self.load_mode](level_data)

    def load_from_json(self, level_data):
        """
        Builds each room from JSON, and creates all nessicary objects
        :param level_data: the data to load from. If not specified, use the data which was provided when the class was instantiated 
        """
        if level_data is None:
            level_data = self.level_data
        json = dict(js_to_the_o_to_the_n.loads(level_data))

        block_data = json["blocks"]
        map_data = json["map"]
        properties = json["properties"]

        for name, data in map_data.items():
            w = len(data[0])
            h = len(data)
            y = 0
            for row in data:
                x = 0
                for col in row:
                    print(col)
            print(name, data)
        print(block_data)
        print(map_data)
        print(properties)
        quit()

    def load_from_xml(self, level_data):
        """
        Builds each room from XML, and creates all nessicary objects
        :param level_data: the data to load from. If not specified, use the data which was provided when the class was instantiated 
        """
        if level_data is None:
            level_data = self.level_data

        self.level_data = level_data
        try:
            json = xmltodict.parse(level_data)
        except xmltodict.expat.ExpatError:
            raise InvalidXMLException("The XML Provided Is Invalid (Syntax Error?). Please Check The XML, And Try Again")
        building = json["building"]["room"]

        sub_rooms = []
        if "subroom" in json["building"]:
            sub_rooms = json["building"]["subroom"]

        if "@name" in building:
            building = [building]
        if "@name" in sub_rooms:
            sub_rooms = [sub_rooms]
        for room in building:
            self.rooms[str(room["@name"])] = Room(self.screen, room, self.custom_objects, self)
        # for sub_room in sub_rooms:
        #     self.sub_rooms[str(sub_room["@name"])] = SubRoom(self.screen, sub_room, self.custom_objects, self)

    def update(self, events:list):
        """
        Triggers the selected room's update event
        :param events: a list of active events
        """
        self.room.update(events)

    def draw(self):
        """
        Triggers the selected room's draw event. Only objects on screen are drawn
        """
        self.room.draw()

    def set_room(self, room):
        """
        Set the selected room to a different room. Triggers the room leave, and enter event
        :param room: the room to move to
        """
        if self.room is not None:
            self.room.leave_room(room)
        try:
            self.room = self.rooms[room]
        except KeyError:
            raise RoomNotDeclaredException(
                "The Specified Room '{}' Has Not Been Declared In The Provided XML. NOTE: Names Are Case Sensitive"
                    .format(room)
            )
        self.room.enter_room()

    def set_mouse_cursor(self, method: 'DisplayBase'):
        """
        Sets the mouse cursor to the specified display method (can be an image, spritesheet, text, or any object which extends the PyGE.DisplayMethods.DisplayBase class)
        :param method: the display method to set the cursor as. Use None to reset to the default cursor.
        """
        pygame.mouse.set_visible(method is None)
        self.mouse_cursor = method

    def add_room(self, name):
        """
        Create a new empty room
        :param name: the name to save the room as
        """
        self.rooms[name] = Room(self.screen, {"@name": name}, self.custom_objects, self)
        return self.rooms[name]

    def delete_room(self, name):
        """
        Deletes the specified room
        :param name: the name of the room to delete
        :return: the room which was just deleted
        """
        rm = self.rooms[name]
        del self.rooms[name]
        return rm

    def rename_room(self, old, new):
        """
        Renames the specifed room
        :param old: the current name of the room
        :param new: the new name of the room
        """
        self.rooms[new] = self.rooms[old]
        self.rooms[new].name = new
        self.delete_room(old)

    def reload_room(self, name:str):
        """
        Reloads a specified room
        :param name: the name of the room to reload
        """
        self.rooms[name].reload_room()

    def attempt_quit(self):
        """
        Attempt to close the application.
        This will trigger each object's "onquit" event.
        If any object returns "False" to the "onquit" event, the quit will not happen.
        All object in the selected room will run this event guarenteed
        """
        if self.room.quit_action():
            quit()

    def export_as_xml(self, filename:str):
        """
        Exports the entire project as XML which can be read by the system
        Note that the system will only export properties set in the metadata property
        :param filename: The filename to export as
        """
        xml = "<building>\n"

        for name, room in self.rooms.items():             # type: str, Room
            xml += "\t<room name=\"{}\">\n".format(name)

            for obj in room.props:                      # type: ObjectBase
                xml += "\t\t<{} ".format(type(obj).__name__)

                for key, value in obj.metadata.items():
                    xml += "{}=\"{}\" ".format(key, value)

                xml += "/>\n"

            xml += "\t</room>\n"

        xml += "</building>"

        with open(filename, 'w') as f:
            f.write(xml)
