import sys
import socket
import select
import time


def receive_file(file_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
    print("Waiting for %s" % file_name)

    while True:
        data, address = s.recvfrom(buffer)
        if data:
            file_name = data.strip()

        file = open(file_name, 'wb')

        while True:
            ready = select.select([s], [], [], 4)
            if ready[0]:
                data, address = s.recvfrom(buffer)
                file.write(data)
            else:
                file.close()
                break
        return 0


def send_file(address, file_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes(file_name, 'utf-8'), (ip, port))
    print("Sending %s to Torrent" % file_name)

    file = open(address, "rb")

    data = file.read(buffer)
    while data:
        if s.sendto(data, (ip, port)) > 0:
            data = file.read(buffer)
            time.sleep(0.04)

    s.close()
    file.close()
    return 0


buffer = 128
ip = '127.0.0.1'
port = 8080
try:
    if sys.argv[1] == "-receive":
        f = receive_file(sys.argv[2])  # Receive file with the name requested
        if f != -1:
            print("Fetching %s Finished!" % str(sys.argv[2]))
        else:
            print("File not fetched!")
    elif sys.argv[1] == "-serve":
        ff = send_file(sys.argv[sys.argv.index("-path") + 1],
                       sys.argv[sys.argv.index("-name") + 1])  # Send file with the name requested
        if ff != -1:
            print("File Sent!")
        else:
            print("File not found!")
    else:
        pass  # Exception
except:
    print("Switches not imported properly!\nDetail:\n" + str(sys.exc_info()[0]))
