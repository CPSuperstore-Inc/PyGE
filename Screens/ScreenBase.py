import pygame

class ScreenBase:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def update(self, events:list):
        pass

    def draw(self):
        pass

    def process_input(self, event, pressed_keys):
        pass
