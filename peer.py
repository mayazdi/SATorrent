import sys
import socket
import traceback
import logging


def receive_file(file_name, sc):
    fli = []
    try:
        file = open('hosts', 'r')
        line = file.readline()
        while line:
            dic = eval(line)
            ip = dic['ip']
            port = int(dic['port'])
            sc.sendto(file_name.encode(), (ip, port))
            print(ip)
            print(port)
            line = file.readline()
        print("Waiting for {filename}".format(filename=file_name))
        sc.settimeout(8.0)

        x = sc.recvfrom(2048)
        data = x[0]
        fli.append((data[0], data[1:]))
        # print('receiver ip: ' + sc.getsockname()[0] + ' receiver port: ' + str(sc.getsockname()[1]))

        while True:
            data, address = sc.recvfrom(2048)
            if data.decode() != '\0':
                fli.append((data[0], data[1:]))
                print(fli)
            else:
                break
        print(file_name)
        # Write into file
        file = open(file_name, 'wb')
        i = 0
        for d in sorted(fli, key=lambda x: x[0]):
            if d[0] == i:
                file.write(d[1])
                i += 1
        sc.close()
        file.close()
        return 0
    except OSError:
        logging.error(traceback.format_exc())
        return -1
    except:
        print(str(sys.exc_info()))
        return -1


def send_file(address, file_name, sc):
    file = open('hosts', 'w')
    dic = {'ip': sc.getsockname()[0], 'port': sc.getsockname()[1]}
    print(str(dic))
    file.write(str(dic) + "\n")
    file.close()

    while True:
        try:
            print('waiting for request...')
            x = sc.recvfrom(2048)
            data = x[0].decode()
            addr = x[1]
            print('request received')

            if data == file_name:
                file = open(address, "rb")
                print("Sending {filename} as Torrent Seeder".format(filename=file_name))
                i = 0
                data = file.read(buffer)
                while data:
                    # print('sender ip: ' + sc.getsockname()[0] + ' sender port: ' + str(sc.getsockname()[1]))
                    # print('receiver ip: ' + addr[0] + ' receiver port: ' + str(addr[1]))
                    if sc.sendto(i.to_bytes(1, 'little', signed=False) + data, addr) > 0:
                        print(data)
                        print(len((i.to_bytes(1, 'little', signed=False) + data)))
                        data = file.read(buffer)
                        i += 1
                sc.sendto((bytes('\0', 'utf-8')), addr)
                file.close()
            else:
                print('I don\'t serve request filename')
        except TypeError:
            logging.error(traceback.format_exc())
        except FileNotFoundError:
            return -1
        except:
            print(str(sys.exc_info()[0]))


buffer = 128
ip = '127.0.0.1'
sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sc.bind((ip, 0))  # one available port

try:
    if sys.argv[1] == "-receive":
        f = receive_file(sys.argv[2], sc)  # Receive file with the name requested
        if f != -1:
            print("Fetching {name} Finished!".format(name=str(sys.argv[2])))
        else:
            print("File not fetched!")
    elif sys.argv[1] == "-serve":
        ff = send_file(sys.argv[sys.argv.index("-path") + 1],
                       sys.argv[sys.argv.index("-name") + 1], sc)  # Send file with the name requested
        if ff != -1:
            print("File {filename} Sent!".format(filename=str(sys.argv[sys.argv.index("-name") + 1])))
        else:
            print("File not found!")
    else:
        print("Not a parsable command!")
except Exception as e:
    logging.error(traceback.format_exc())
