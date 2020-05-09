import sys
import socket
import select
import time


def receive_file(file_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 8080))

    while True:
        data, address = sock.recvfrom(1024)
        if data:
            print("File name:", data)
            file_name = data.strip()

        file = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [], 4)
            if ready[0]:
                data, address = sock.recvfrom(1024)
                file.write(data)
            else:
                print("%s Finish!" % file_name)
                file.close()
                break
        return 0


def send_file(address, file_name):
    ip = "127.0.0.1"
    port = 8080
    buf = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(file_name, 'utf-8'), (ip, port))
    print("Sending %s ..." % file_name)

    file = open(address, "rb")

    data = file.read(buf)
    while data:
        if sock.sendto(data, (ip, port)):
            data = file.read(buf)
            time.sleep(0.04)

    sock.close()
    file.close()
    return 0


try:
    if sys.argv[2] == "-receive":
        f = receive_file(sys.argv[2])  # Receive file with the name requested
        if f != -1:
            print("File saved!")
        else:
            print("File not fetched!")
    elif sys.argv[2] == "-serve":
        ff = send_file(sys.argv[sys.argv.index("-path") + 1],
                       sys.argv[sys.argv.index("-name") + 1])  # Address to save fetched file
        if ff != -1:
            print("File Sent!")
        else:
            print("File not found!")
    else:
        pass  # Exception
except:
    print("Switches not imported properly!\nDetail:\n" + str(sys.exc_info()[0]))
