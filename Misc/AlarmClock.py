import time


class AlarmClock:
    def __init__(self, duration:float, start:bool=False):
        self.duration = duration
        self.start_time = None
        if start:
            self.start()

    def start(self):
        self.start_time = time.time()

    @property
    def time(self):
        return time.time() - self.start_time

    @property
    def finished(self):
        return time.time() - self.start_time >= self.duration

    def restart(self):
        self.start()

    def stop(self):
        self.start_time = None

    @property
    def running(self):
        return self.start_time is not None
