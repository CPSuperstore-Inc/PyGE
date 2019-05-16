import pygame

CHANNELS = 8
pygame.mixer.init(channels=CHANNELS)

channels = []

for c in range(CHANNELS):
    channels.append(pygame.mixer.Channel(c))


def get_free_channel():
    index = -1
    for chan in channels:
        index += 1
        if chan.get_busy() == 0:
            return chan


def playsound(sound):
    chan = get_free_channel()
    chan.play(sound)
