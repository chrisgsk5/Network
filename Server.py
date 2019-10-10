# Echo server program
import socket
import struct
import random

HOST = ''               # Symbolic name meaning all available interfaces
PORT = 12235              # Arbitrary non-privileged port
HEADERLEN = 12
TIMEOUT = 5

def get_info(data, secret):
    header, message = data[:HEADERLEN], data[HEADERLEN:]
    payload_len, psecret, step, sid = struct.unpack("!IIHH", header)
    message = message[:payload_len]
    if len(data) % 4 != 0:
        raise ValueError('Invalid message length')
    elif psecret != secret:
        raise ValueError('Invalid psecret. Need {}, got {}'.format(secret, psecret))
    elif step != 1:
        raise ValueError('Invalid step. Need 1, got {}'.format(step))
    return payload_len, psecret, step, sid, message
    #  = header[]

def checkZeros(payload):
    for b in payload:
        if b != b'0':
            return False
    return True

def get_socket(type):
    if type == 'udp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    elif type == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        raise ValueError('Illegal socket type')
    port = random.randint(49152, 65535)
    success = False
    while not success:
        try:
            sock.bind(('', port))
            success = True
        except:
            pass
    return port, sock

def main():
    su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
    # st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    su.bind((HOST, PORT))
    # su.listen(1)
    # conn, addr = su.accept()
    # print('Connected by', addr)
    while 1:
        # a1
        data, client = su.recvfrom(1024)
        print(data)
        payload_len, psecret, step, sid, message = get_info(data, 0)
        if message != b'hello world\0':
            raise ValueError('Invalid message. '
                             'Need hello world, got {}'.format(message))

        # a2
        header = struct.pack("!IIHH", 16, 0, 1, sid)
        port, su = get_socket('udp')
        num, len, udp_port, secretA = random.randint(1, 10), random.randint(1, 20), \
                              port, random.randint(0, 400)
        payload = struct.pack("!IIII", num, len, udp_port, secretA)
        su.sendto(header + payload, client)


        # b1
        # su.bind((HOST, udp_port))
        su.settimeout(TIMEOUT)
        i = 0
        metPacket = -1
        while i < num:
            print('b', i)
            try:
                print("Before")
                data= su.recv(1024)
                print("After")
            except:
                raise ValueError('Did not recieve data')
            else:
                payload_len, psecret, step, sid, message = get_info(data, secretA)
                print("Got ", payload_len, psecret, step, sid, message)
                pid = struct.unpack('!I', message[:4])
                payload = message[4:]
                if payload_len != len + 4:
                    raise ValueError('Message length should be {}, got {}'.format(len + 4,
                                                                                  payload_len))
                elif i != pid:
                    raise ValueError('Pid error. Should be {}, got {}'.format(i, pid))
                elif not checkZeros(payload):
                    raise ValueError('Not all payload are 0s')
                if pid == metPacket:
                    print('Received ', i)
                    if random.randint(0, 1) == 1:
                        header = struct.pack("!IIHH", 16, 0, 1, sid)
                        payload = struct.pack("!I", i)
                        print('Sent', i)
                        su.sendto(header + payload, client)
                        i += 1
                    else:
                        metPacket = i

        # b2
        header = struct.pack("!IIHH", 16, 0, 1, sid)
        tcp_port, secretB = random.randint(49152, 65535), random.randint(0, 400)
        payload = struct.pack("!II", tcp_port, secretB)
        su.sendto(header + payload, client)







        # if not data: break
        # conn.sendall(data)
    # conn.close()

if __name__ == '__main__':
    main()