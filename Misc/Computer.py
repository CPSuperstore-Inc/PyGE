from screeninfo import get_monitors


def get_monitor_resolution(monitor:int=0):
    selected_monitor = get_monitors()[monitor]
    return selected_monitor.width, selected_monitor.height
