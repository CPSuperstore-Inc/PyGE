import threading

VARIABLES = {
    "loaded": False,
    "current_pitch": 0.0
}
threads = []

def new_thread(action:callable, name, start, *args, **kwargs):
    p = threading.Thread(
        target=action,
        name=name,
        args=args,
        kwargs=kwargs
    )
    if start:
        p.start()
    threads.append(p)
    return p

def set_var(key, value):
    """
    Sets a global variable
    :param key: The name of the variable
    :param value: The value of the variable
    """
    VARIABLES[key] = value

def get_var(key):
    """
    Returns a global variable
    :param key: The name of the variable
    :return: The value of the variable
    """
    return VARIABLES[key]

def get_vars():
    """
    Returns all of the saved variables
    :return: A dictionary of each variable
    """
    return VARIABLES

def show_vars():
    """
    Prints all of the variables and values to the console in Name/Value format
    """
    print(VARIABLES)


#
# WARNING:
# SYS VARIABLES ARE PRIVATE
# AND SHOULD NOT BE GIVEN A DOCSTRING!
#

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
