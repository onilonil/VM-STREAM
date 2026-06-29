"""
payload 封包
payload 解包

length （4byte）  ---->  payload


"""

import struct

# I = unsigned int 4 byte
HEADER_FORMAT = "!I"

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def pack(payload:bytes) -> bytes:
    """
    将数据封装成网路数据包
    :param payload:
    :return: Header + payload 放回I 和封装好的内容，I I为包含这个内容大小的信息 4byte
    """

    header = struct.pack(HEADER_FORMAT,len(payload))

    return header + payload


def unpack_header(header:bytes) -> int :
    """
    解包header
    :param header: 4byte

    :return: payload 长度
    """
    (length,)= struct.unpack(HEADER_FORMAT,header)

    return length


