import pygame

from SideScroller.Globals.GlobalVariable import get_var

def get_optional(dic: dict, key: str, default, return_type:type=None):
    if key in dic:
        val = dic[key]
    else:
        val = default

    if return_type is not None:
        val = return_type(val)
    return val


def get_mandatory(dic: dict, key: str, return_type:type=None):
    if key in dic:
        if return_type is None:
            return dic[key]
        return return_type(dic[key])
    raise ValueError("You Suck And Can Not Extract Key {} From {}".format(key, dic))


def rect_a_touch_b(rect_a: tuple, rect_b: tuple):
    # if rects touch (any overlap)
    a_x, a_y, a_w, a_h = rect_a
    b_x, b_y, b_w, b_h = rect_b

    points = [
        (a_x, a_y),
        (a_x + a_w, a_y),
        (a_x + a_w, a_y + a_h),
        (a_x, a_y + a_h)
    ]

    for x, y in points:
        if b_x < x < b_x + b_w and b_y < y < b_y + b_h:
            return True
    return False


def rect_a_in_b(rect_a: tuple, rect_b: tuple):
    # if A is fully inside b
    a_x, a_y, a_w, a_h = rect_a
    b_x, b_y, b_w, b_h = rect_b

    points = [
        (a_x, a_y),
        (a_x + a_w, a_y),
        (a_x + a_w, a_y + a_h),
        (a_x, a_y + a_h)
    ]

    for x, y in points:
        if not (b_x < x < b_x + b_w and b_y < y < b_y + b_h):
            return False
    return True


def point_in_rect(point: tuple, rect: tuple):
    # if rects touch (any overlap)
    x, y = point
    b_x, b_y, b_w, b_h = rect
    return b_x < x < b_x + b_h and b_y < y < b_y + b_h


def deconstruct_modifier_bitmask(modifier):
    modifiers = []
    mods = [
        pygame.KMOD_NONE, pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT, pygame.KMOD_SHIFT, pygame.KMOD_LCTRL,
        pygame.KMOD_RCTRL, pygame.KMOD_CTRL, pygame.KMOD_LALT, pygame.KMOD_ALT, pygame.KMOD_LMETA, pygame.KMOD_RMETA,
        pygame.KMOD_NUM, pygame.KMOD_CAPS, pygame.KMOD_MODE
    ]
    for mod in mods:
        if modifier & mod:
            modifiers.append(mod)
    return modifiers


def scale_image(image:pygame.Surface):
    return image
    # new_h = int(round(image.get_height() * get_var("scale-factor"), 0))
    # new_w = int(round(image.get_width() * get_var("scale-factor"), 0))
    # return pygame.transform.scale(image, (new_w, new_h))

def scale_coords(coords:tuple, factor:float=None):
    if factor is None:
        # factor = get_var("scale-factor")
        return coords

    divider = 3
    coords = safe_int(coords[0] * (factor / divider)), safe_int(coords[1] * (factor / divider))
    return coords

def safe_int(val: float):
    return int(round(val, 0))
