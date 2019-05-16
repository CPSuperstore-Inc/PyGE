import pygame

from SideScroller.Objects.ObjectBase import ObjectBase
from SideScroller.Screens.Room import Room
from SideScroller.utils import get_optional, get_mandatory
from SideScroller.Globals.Cache import get_sound
from SideScroller.Audio import get_free_channel


class Sound(ObjectBase):
    def __init__(self, screen:pygame.Surface, args: dict, parent:'Room'):
        args["@x"] = 0
        args["@y"] = 0
        ObjectBase.__init__(self, screen, args, parent)

        self.src = get_mandatory(args, "@src", str)
        self.repetitions = get_optional(args, "@repeat", 0, int)
        self.channel = get_free_channel()

        self.playing = True

        self.repetition = -1
        self.sound = get_sound(self.src)

    def update(self, pressed_keys):
        if self.channel.get_busy() == 0:
            if (self.repetition < self.repetitions or self.repetitions == -1) and self.playing:
                self.channel.play(self.sound)
                self.repetition += 1
    def stop(self):
        self.playing = False
        self.sound.stop()
        self.channel.stop()

    def onroomleave(self, next_room):
        self.sound.stop()
        self.channel.stop()
