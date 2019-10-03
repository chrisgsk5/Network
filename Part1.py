# Echo client program
import socket
import struct
import time

def pads(num, byt=struct.pack("I", 0)):
    res = b''
    while num > 0:
        # print(len(res))
        res += byt
        num -= 1
    return res

def send_recur(s, packet):
    try:
        s.send(packet)
        data = s.recv(1024)
    except:
        send_recur(s, packet)
    else:
        return data

def main():
    HOST = 'attu2.cs.washington.edu'    # The remote host
    PORT = 12235              # The same port as used by the server
    su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

    # Step a
    def stageA():
        su.connect((HOST, PORT))
        payload_len, pSec, step, stuNum = 12, 0, 1, 385
        header = struct.pack("!IIHH", payload_len, pSec, step, stuNum)
        message = b'hello world\0'
        print(len(header + message))
        su.send(header + message)
        data = su.recv(1024)
        print('a Received', repr(data), len(data))
        # su.close()

        data = data[12:]
        print(len(data))
        return data


    # Step b
    def stageB():
        su.connect((HOST, udp_port))
        su.settimeout(0.5)
        payload_len, pSec, step, stuNum = blen + 4, secretA, 1, 385
        header = struct.pack("!IIHH", payload_len, pSec, step, stuNum)
        message = pads(blen + blen % 4)
        cnt = 0
        while cnt < num:

            print(blen, 4 - blen % 4, cnt)
            message = struct.pack("!I", cnt) + message
            packet = header + message
            print(header, message, len(packet))
            data = send_recur(su, packet)
            print('Received', repr(data))
            cnt += 1

        data = su.recv(1024)
        print('b Received', repr(data), len(data))
        su.close()

        data = data[12:]
        return data


    # Stage c
    def stageC():
        st.connect((HOST, tcp_port))
        data = st.recv(1024)
        data = data[12:-3]
        print('c Received', len(data), data)
        return data

    def stageD():
        header = struct.pack("!IIHH", len2, secretC, 1, 385)
        message = pads(len2, struct.pack("c", c))
        print(c, message)
        for _ in range(num2):
            st.send(header + message)
        data = st.recv(1024)[12:]
        st.close()
        print('d Received', data)
        return data



    num, blen, udp_port, secretA = struct.unpack("!IIII", stageA())
    print(num, blen, udp_port, secretA)
    tcp_port, secretB = struct.unpack("!II", stageB())
    print(tcp_port, secretB)
    num2, len2, secretC, c = struct.unpack("!IIIc", stageC())
    print(num2, len2, secretC, c)
    secretD = struct.unpack("!I", stageD())[0]
    print(secretD)
    # c = b'\x11'
    # print(chr(int.from_bytes(c, "big")))



if __name__ == '__main__':
    main()