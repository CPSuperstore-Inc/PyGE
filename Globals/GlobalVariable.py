VARIABLES = {
    "loaded": False
}

def set_var(key, value):
    VARIABLES[key] = value

def get_var(key):
    return VARIABLES[key]

def get_vars():
    return VARIABLES

def show_vars():
    print(VARIABLES)


SYS_VARS = {
    "debug": False,
    "debug-color": (255, 255, 255)
}

def set_sys_var(key, value):
    SYS_VARS[key] = value

def get_sys_var(key):
    return SYS_VARS[key]

def get_sys_vars():
    return SYS_VARS

def show_sys_vars():
    print(SYS_VARS)