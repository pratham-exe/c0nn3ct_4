import socket
import ssl
import sys

global Host

Host = input("Enter Host IP : ")
Port1 = int(input("Enter Port 1 : "))
Port2 = int(input("Enter Port 2 : "))


def bind_socket(port, s):
    try:
        print("Binding the socket")
        s.bind((Host, port))
        s.listen()
    except socket.error as mag:
        print("Socket binding error ", str(mag), "Retrying")
        bind_socket(port, s)


def accept(s):
    conn, adress = s.accept()
    ssl_server = ssl_context.wrap_socket(conn, server_side=True)
    ssl_server.setblocking(True)
    print("Ip: ", adress[0], " Port: ", adress[1])

    return ssl_server


def s1_to_s2():
    data = conn1.recv(2048).decode()
    if (data == '100'):
        sys.exit()
    conn2.sendall(data.encode())


def s2_to_s1():
    data = conn2.recv(2048).decode()
    if (data == '100'):
        sys.exit()

    conn1.sendall(data.encode())


if __name__ == "__main__":
    turn = 0
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='./server_cert.pem', keyfile='./server_key.pem')

    bind_socket(Port1, s1)
    conn1 = accept(s1)

    bind_socket(Port2, s2)
    conn2 = accept(s2)

    while (True):
        if (turn % 2 == 0):
            s1_to_s2()
            turn += 1
        else:
            s2_to_s1()
            turn += 1
