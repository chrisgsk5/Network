# Echo server program
import socket

HOST = ''               # Symbolic name meaning all available interfaces
PORT = 12235              # Arbitrary non-privileged port

def main():
    su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    su.bind((HOST, PORT))
    # su.listen(1)
    # conn, addr = su.accept()
    # print('Connected by', addr)
    while 1:
        data, sender = su.recv(1024)
        if not data: break
        # conn.sendall(data)
    # conn.close()

if __name__ == '__main__':
    main()