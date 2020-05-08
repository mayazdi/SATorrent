import sys


def receive_file(f):
    # pass # Return the downloaded file or return -1


def save_file(addr):
    pass # Save the file in the requested address


def to_file(addr):
    pass # Turn address to file and if not found return -1


def serve_file(f):
    pass # Serve the file passed


try:
    if sys.argv[1]=="-receive":
        f = receive_file(sys.argv[2]) # Receive file with the name requested
        if f == -1:
            print("File not fetched!")
        else:
            save_file(f)
            print("File saved!")
    elif sys.argv[1]=="-serve":
        # sys.argv[sys.argv.index("-name")+1] # Name of the served file if needed
        ff = to_file(sys.argv[sys.argv.index("-path")+1]) # Address to save fetched file
        if ff == -1:
            print("File not found!")
        else:
            serve_file(ff)
            print("File Snet!")
    else:
        pass # Exception
except:
    print("Switches not imported properly!\nDetail:\n" + sys.exc_info()[0])

