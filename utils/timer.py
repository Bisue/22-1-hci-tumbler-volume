import time


class CustomTimer:
    def __init__(self):
        self.timer_seconds = 5
        self.processing = False
        self.prev = 0

    def is_capturing(self):
        return self.processing

    def start_timer(self, seconds):
        self.timer_seconds = seconds
        self.processing = True
        self.prev = time.time()

    def process_timer(self):
        cur = time.time()

        if cur - self.prev >= 1:
            self.prev = cur
            self.timer_seconds -= 1

        return self.timer_seconds

    def done(self):
        return self.timer_seconds <= 0

