import pygame

class ScreenBase:
    def __init__(self, screen: pygame.Surface):
        """
        The base class for all screens
        :param screen: The pygame surface to draw the screen to
        """
        self.screen = screen

    def update(self, events:list):
        """
        All of the update, and processing code should go here
        :param events: A list of all of the pygame events detected since the last call
        """
        pass

    def draw(self):
        """
        All of the graphical updates should go here
        """
        pass

    def process_input(self, event, pressed_keys):
        """
        Processes keyboard input
        :param event: The pygame events
        :param pressed_keys: The list of the states of each key. Indexes are based on ASCII values. Ex. 101=e, so pressed_keys[101] = state of the 'e' key
        :return: 
        """
        pass
