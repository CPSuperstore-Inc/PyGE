import threading
import time
import typing

import pygame

from SideScroller.Globals.Cache import set_spritesheet, set_image, set_sound
from SideScroller.Globals.GlobalVariable import set_var, set_sys_var
from SideScroller.Misc.Computer import get_monitor_resolution
from SideScroller.SideScroller import SideScroller
from SideScroller.utils import get_optional


def side_scroller(
        xml:str, start_room:str, images=None, sprite_sheets=None, sounds=None, development_screen_size:tuple=None, refresh_rate:int=60,
        caption:str= "Python Side Scroller Engine", icon:str=None, loading_screen:callable=None, min_loading_time:int=0,
        custom_objects:typing.List=None, enable_alt_f4:bool=True, initial_variables=None, fullscreen:bool=True,
        debug:bool=False, debug_color:tuple=(255, 255, 255), auto_scale:bool=True
):

    set_sys_var("debug", debug)
    set_sys_var("debug-color", debug_color)

    def termanate():
        if game.room.quit_action():
            quit()

    if initial_variables is None:
        initial_variables = {}

    for name, value in initial_variables.items():
        set_var(name, value)

    if custom_objects is None:
        custom_objects = []

    if development_screen_size is None:
        development_screen_size = get_monitor_resolution()

    game_screen_size = get_monitor_resolution()

    x_scale = game_screen_size[0] / development_screen_size[0]
    y_scale = game_screen_size[1] / development_screen_size[1]

    scale_factor = 1

    if development_screen_size[0] * y_scale <= game_screen_size[0]:
        scale_factor = y_scale
    elif development_screen_size[1] * x_scale <= game_screen_size[1]:
        scale_factor = x_scale
    else:
        quit()

    scaled_size = (
        int(development_screen_size[0] * scale_factor),
        int(development_screen_size[1] * scale_factor)
    )
    scaled_pos = (
        (game_screen_size[0] / 2) - (scaled_size[0] / 2),
        (game_screen_size[1] / 2) - (scaled_size[1] / 2)
    )

    mode = 0
    if fullscreen: mode = pygame.FULLSCREEN

    if auto_scale:
        main_surf = pygame.display.set_mode(game_screen_size, mode)
    else:
        main_surf = pygame.display.set_mode(development_screen_size, mode)

    screen = pygame.Surface(development_screen_size)

    pygame.display.set_caption(caption)

    if loading_screen is not None:
        t = threading.Thread(
            target=loading_screen,
            args=(screen,)
        )
        t.setDaemon(True)
        t.start()

    load_start = time.time()

    if sprite_sheets is None:
        sprite_sheets = {}

    if images is None:
        images = {}

    if sounds is None:
        sounds = {}

    if icon is not None:
        pygame.display.set_icon(pygame.image.load(icon))

    for name, props in images.items():
        set_image(name, props['path'], get_optional(props, "w", None), get_optional(props, "h", None))

    for name, props in sprite_sheets.items():
        set_spritesheet(name, props["path"], props["w"], props["h"], props["duration"], get_optional(props, "final_size", None), get_optional(props, "invisible_color", (0, 0, 1)))

    for name, props in sounds.items():
        set_sound(name, props["path"], get_optional(props, "volume", 1.0, float))

    clock = pygame.time.Clock()
    game = SideScroller(screen, xml, start_room, custom_objects)

    load_duration = time.time() - load_start
    if load_duration < min_loading_time:
        time.sleep(min_loading_time - load_duration)

    set_var("loaded", True)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                termanate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT or event.mod & pygame.KMOD_RALT) and enable_alt_f4:
                    termanate()


        screen.fill((0, 0, 0))
        game.update(events)
        game.draw()

        if auto_scale:
            main_surf.blit(pygame.transform.scale(screen, scaled_size), scaled_pos)
        else:
            main_surf.blit(screen, (0, 0))

        pygame.display.update()

        clock.tick(refresh_rate)
