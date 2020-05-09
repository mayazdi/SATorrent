import sys
import socket
import select
import time
import traceback
import logging
import hashlib

def receive_file(file_name):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((ip, port))
        print("Waiting for {filename}".format(filename = file_name))

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
            fhsh = open(file_name, 'rb')
            return hashlib.md5(fhsh.read()).hexdigest()
    except:
        print(str(sys.exc_info()[0]))
        return -1


def send_file(address, file_name):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(bytes(file_name, 'utf-8'), (ip, port))
        print("Sending {filename} as Torrent Seeder".format(filename = file_name))

        file = open(address, "rb")

        data = file.read(buffer)
        while data:
            if s.sendto(data, (ip, port)) > 0:
                data = file.read(buffer)
                time.sleep(0.04)

        s.close()
        file.close()
        file = open(address, "rb")
        fhsh = hashlib.md5(file.read()).hexdigest()
        file.close()
        return fhsh
    except:
        print(str(sys.exc_info()[0]))
        return -1


buffer = 4096
ip = '127.0.0.1'
port = 8080
try:
    if sys.argv[1] == "-receive":
        f = receive_file(sys.argv[2])  # Receive file with the name requested
        if f != -1:
            print("Fetching {name} Finished!".format(name=str(sys.argv[2])))
            print("Hash: " + f)
        else:
            print("File not fetched!")
    elif sys.argv[1] == "-serve":
        ff = send_file(sys.argv[sys.argv.index("-path") + 1],
                       sys.argv[sys.argv.index("-name") + 1])  # Send file with the name requested
        if ff != -1:
            print("File Sent!")
            print("Hash: " + ff)
        else:
            print("File not found!")
    else:
        print("Not a parsable command!")
except Exception as e:
    logging.error(traceback.format_exc())
