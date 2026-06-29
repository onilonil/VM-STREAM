import numpy as np
import av
import cv2

from VMStream.logger import get_logger
from fractions import Fraction
from collections.abc import Iterator


logger = get_logger("codec")

class JPEGCodec:
    """
    JPEG ---> Encode ---> Decode ----> Receiver
    """
    @staticmethod
    def encode(image:np.ndarray) -> bytes:
        success, encoded_img = cv2.imencode('.jpg', image)
        if not success:
            raise RuntimeError("JPEG 编码失败")
        return encoded_img.tobytes()

    @staticmethod
    def decode(payload:bytes) ->np.ndarray:
        np_arr = np.frombuffer(payload, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            raise RuntimeError("JPEG 解码失败")
        return img


class H264Encoder:
    """
    Encode one BGR image to h.264 packets
    Args: image :open_cv bgr image
    Yields: Encoded h.264 packets
    """

    def __init__(self,fps:int=30,bitrate:int=8_000_000) -> None:
        """
        H.264 encoder
        input: bgr frame
        output: h264 Annex-b bytes

        """
        self._codec = None
        self.fps = fps
        self.bitrate = bitrate
        self._width = None
        self._height = None
        self._closed = False

    def _open(self,image):
        self._height,self._width = image.shape[:2]

        self._codec = av.CodecContext.create("libx264", "w")
        self._codec.width = self._width
        self._codec.height = self._height
        self._codec.pix_fmt = "yuv420p"
        self._codec.framerate = Fraction(self.fps,1)
        self._codec.time_base = Fraction(1,self.fps)

        self._codec.bit_rate = self.bitrate

        self._codec.max_b_frames =0
        self._codec.gop_size = 30
        self._codec.options = {
            "preset":"veryfast",
            "tune":"zerolatency",
            "crf":"20"
        }
        logger.info("H264 encoder initialized(%dx%d @ %dfps)",
                    self._width,
                    self._height,
                    self.fps)
        self._codec.open()




    def encode(self,image:np.ndarray) -> Iterator[bytes]:
        if self._codec is None :
            self._open(image)

        self._validate_image(image)

        frame = av.VideoFrame.from_ndarray(image,format="bgr24")

        packets = self._codec.encode(frame)

        for packet in packets:
            yield bytes(packet)


    def flush(self) -> Iterator[bytes]:
        if self._codec is None:
            return

        for packet in self._codec.encode(None):
            yield bytes(packet)

    def close(self) -> None:
        if self._codec is None:
            return
        logger.info("encoder closed")
        self._codec = None
        self._closed = True


    def _validate_image(self,image:np.ndarray) -> None:

        if image is None:
            logger.info("image is None")
            raise ValueError("image can't be None")

        if not isinstance(image,np.ndarray):
            logger.info("image type is wrong")
            raise TypeError("image must be a numpy array")

        if image.dtype != np.uint8:
            logger.info("image dtype is not np.unit8")
            raise ValueError("image dtype must be np.uint8")

        h,w = image.shape[:2]
        if h != self._height or w != self._width:
            logger.info("image size not matched")
            raise ValueError("image size must match")


class H264Decoder:
    """
    Decode h.264 payload into images
    Args: payload : Encoded h.264 packet (bytes)
    Yields: opencv bgr image
    """
    def __init__(self):
        self._codec = av.CodecContext.create("h264","r")
        self._codec.open()
        logger.info("h264 decoder initialized")
        self._closed = False

    def decode(self,payload:bytes) ->Iterator[np.ndarray]:

        packet = av.Packet(payload)

        for frame in self._codec.decode(packet):

            yield frame.to_ndarray(format="bgr24")

    def flush(self) -> Iterator[np.ndarray]:
        for frame in self._codec.decode(None):
            yield frame.to_ndarray(format="bgr24")

    def close(self) -> None:
        self._codec = None
        if self._codec is None:
            return
        logger.info("decoder closed")
        self._codec = None
        self._closed =True