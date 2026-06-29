import cv2

from VMStream.statistics import StreamStatistics

from VMStream.transport import create_server,recv_packet

from VMStream.codec import H264Decoder
from VMStream.logger import get_logger
from VMStream.config import HOST,PORT

logger = get_logger("receiver")
class Receiver:
    def __init__(self):

        self.server = create_server(HOST,PORT)

        logger.info("Waiting sender...")

        self.sock,self.addr = self.server.accept()

        logger.info("connected: %s",self.addr)
        self.decoder = H264Decoder()

        self.stats = StreamStatistics()

    def run (self):
        try:
            while True:

                payload = recv_packet(self.sock)

                for image in  self.decoder.decode(payload):
                    self.stats.add_frame()
                    cv2.imshow("VMstream",image)

                    if self.stats.update():
                        logger.info("FPS:%.1f",self.stats.fps)

                if cv2.waitKey(1) == 27:
                    break
        except  KeyboardInterrupt:
            logger.info("stop stream")

    def close(self):
        logger.info("stopping receiver...")
        for image in self.decoder.flush():
            cv2.imshow("VM|Stream", image)

        self.decoder.close()
        self.sock.close()
        self.server.close()
        cv2.destroyAllWindows()
        logger.info("receiver closed")


def main():
    receiver = Receiver()
    try:
        receiver.run()
    except KeyboardInterrupt:
        logger.info("keyboardInterrupt")
    finally:
        receiver.close()

if __name__ == "__main__":
    main()


