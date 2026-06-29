import time

class StreamStatistics:
    def __init__(self):
        self._frames = 0
        self._packets = 0
        self._bytes =0

        self._fps =0.0
        self._bitrate =0.0
        self._last_time =time.perf_counter()

    def add_frame(self):
        self._frames += 1

    def add_packet(self,size:int):
        self._packets += 1
        self._bytes += size

    def update(self):
        now = time.perf_counter()
        elapsed = now - self._last_time
        if elapsed < 1.0:
            return False

        self._fps = self._frames/elapsed
        self._bitrate = self._bytes * 8/elapsed

        self._frames = 0
        self._packets = 0
        self._bytes = 0

        self._last_time = now

        return True

    @property
    def fps(self):
        return self._fps

    @property
    def bitrate(self):
        return self._bitrate

    @property
    def packets(self):
        return self._packets

