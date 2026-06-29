import cv2
import numpy as np

from VMStream.logger import get_logger

logger = get_logger("capture")
class CameraCapture:
    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            logger.info("cannot open camera")
            raise RuntimeError("无法打开摄像头")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        logger.info("start stream")

    def read(self) ->np.ndarray:
        rec,frame = self.cap.read()
        if not rec:
            logger.info("camera not single")
            raise RuntimeError("读取视频帧失败")

        return frame

    def release(self):
        self.cap.release()
        logger.info("stop stream")