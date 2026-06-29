from VMStream.worker import CaptureThread,EncodeThread
from VMStream.codec import H264Encoder
from VMStream.statistics import StreamStatistics
from VMStream.transport import send_packet,create_client
from VMStream.logger import get_logger
from VMStream.config import *
from queue import Queue
import time


logger = get_logger("sender")
class Sender:
    def __init__(self):

        self.encoder = H264Encoder()
        self.sock = create_client(HOST,PORT)
        logger.info("Connected to receiver: %s",self.sock)
        self.stats = StreamStatistics()
        self.queue = Queue(maxsize=QUEUE_SIZE)
        self.capture_thread = CaptureThread(self.queue)
        self.encode_thread = EncodeThread(self.queue,
                                          self.encoder,self.sock,self.stats)

    def run(self):
        self.capture_thread.start()
        self.encode_thread.start()
        try:
            while True:
                    time.sleep(1)
                    if self.stats.update():
                        logger.info("Bitrate:%2f Mbps",self.stats.bitrate / 1_000_000)

        except KeyboardInterrupt:
            logger.info("keyboardInterrupt")

        finally:
            self.close()

    def close(self):
        logger.info("stopping sender...")
        self.capture_thread.stop()
        self.encode_thread.stop()
        self.capture_thread.join()
        self.encode_thread.join()

        for payload in self.encoder.flush():
            send_packet(self.sock, payload)
        self.encoder.close()
        self.sock.close()
        logger.info("sender closed:%s", self.sock)

def main():
    sender = Sender()
    try:
        sender.run()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt")
    finally:
        sender.close()

if __name__ == "__main__":
    main()