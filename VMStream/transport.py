"""

TCP通行
发送数据包
接受数据包

"""
import struct
import socket

from  VMStream.protocol import  pack,unpack_header ,HEADER_SIZE


def create_server(host:str,port:int) -> socket.socket:
    """
    创见TCP服务端
    :param host:
    :param port:
    :return:
    """
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    server.bind((host,port))
    server.listen(1)

    return server
def create_client(host:str,port:int) -> socket.socket:
    """
    创建TCP客户端
    :param host:
    :param port:
    :return:
    """
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))

    return client


def recv_exactly(sock:socket.socket,size:int) -> bytes:
    """
    从socket 精确接受指定长度的数据
    :param sock: socket对象
    :param size: 需要接受的字节数
    :return: bytes
    """

    buffer = bytearray()

    while len(buffer) < size:
        chunk = sock.recv(size - len(buffer))

        if not chunk:
            raise ConnectionResetError("断开连接")
        buffer.extend(chunk)


    return bytes(buffer)

def send_packet(sock:socket.socket,payload:bytes) -> None :
    """
    发送完整数据包

    """
    header = struct.pack("!I", len(payload))

    print("Send Header:", header.hex(), len(payload))
    packet = pack(payload)
    sock.sendall(packet)


def recv_packet(sock:socket.socket) -> bytes:
    """
    接受完整数据包
    :param sock:
    :return: payload、内容
    """
    header= recv_exactly(sock,HEADER_SIZE)

    payload_size = unpack_header(header)

    payload = recv_exactly(sock,payload_size)

    return payload

