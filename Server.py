# Echo server program
import socket
import struct
import random

HOST = ''               # Symbolic name meaning all available interfaces
PORT = 12235              # Arbitrary non-privileged port
HEADERLEN = 12

def check_message(data, secret):
    header, message = data[:HEADERLEN], data[HEADERLEN:]
    payload_len, psecret, step, sid = struct.unpack("!IIHH", header)
    message = message[:payload_len]
    if payload_len % 4 != 0:
        raise ValueError('Invalid message length')
    elif psecret != secret:
        raise ValueError('Invalid psecret. Need 0, got {}'.format(psecret))
    elif step != 1:
        raise ValueError('Invalid step. Need 1, got {}'.format(step))
    return message, sid
    # num, len, udp_port, secretA = header[]




def main():
    su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    su.bind((HOST, PORT))
    # su.listen(1)
    # conn, addr = su.accept()
    # print('Connected by', addr)
    while 1:
        # a1
        data, client = su.recvfrom(1024)
        message, sid = check_message(data, 0)
        if message != b'hello world\0':
            raise ValueError('Invalid message. '
                             'Need hello world, got {}'.format(message))
        # a2
        header = struct.pack("!IIHH", 16, 0, 1, sid)
        payload = struct.pack("!IIII", random.randint(0, 20), random.randint(0, 20),
                              random.randint(49152, 65535), random.randint(0, 400))
        su.sendto(header + payload, client)



        # if not data: break
        # conn.sendall(data)
    # conn.close()

if __name__ == '__main__':
    main()