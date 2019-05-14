import time
from math import *


class Function:
    def __init__(self, func:str):
        self.func = func
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_y(self, x=None):
        if x is None:
            x = time.time() - self.start
        return eval(self.func.replace("x", str(x)))