from threading import Thread,Event
from queue import Queue,Empty,Full
from VMStream.capture import CameraCapture
from VMStream.transport import send_packet
from VMStream.logger import get_logger


logger = get_logger("thread")

class WorkerThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)

        self._running = Event()
        self._running.set()


    @property
    def running(self):
        return self._running.is_set()
    def stop(self):
        self._running.clear()

class CaptureThread(WorkerThread):
    def __init__(self,queue:Queue):
        super().__init__()

        self.queue = queue
        self.capture = CameraCapture()

    def run(self):
        logger.info("capture thread start")
        while self.running :
            image = self.capture.read()
            try:
                self.queue.put_nowait(image)
            except Full:
                try:
                    self.queue.get_nowait()
                except Empty:
                    pass
                self.queue.put_nowait(image)
        self.capture.release()
        logger.info("capture thread closed")


class EncodeThread(WorkerThread):
    def __init__(self, queue, encoder, sock, stats):
        super().__init__()
        self.queue = queue
        self.encoder = encoder
        self.sock = sock
        self.stats = stats

    def run(self):
        while self.running:
            try:
                frame = self.queue.get(timeout=0.1)
                print("get frame")
            except Empty:
                continue

            for payload in self.encoder.encode(frame):
                send_packet(self.sock, payload)

                self.stats.add_packet(len(payload))