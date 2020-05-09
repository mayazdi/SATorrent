# Seyyed & Amin Torrent
Computer Networking Project number 1

Simple file sharing system using UDP connection in python

## Requirements
Any version of Python 3


## Discription
This `peer.py` can be used to send and receive file both. receiver or sender mode can be set as running switch command.
This is just a __test__, So the IP address and port number is set to `localhost` and `8080` (Not that this port must not be used by any other service).
Clearly in order to use this rogram in real case, IP and Port must be set some other values.


## Usage

### As server (Seeder)
`python peer.py –serve -name hello.txt -path D:\hello.txt`

The name after switch `-serve` will put the program in the Server mode
Server will serve the file in the directory mentioned after `-path` **(Note that address can not include any space characters)**


### As Client

`python peer.py –receive hello.txt`

The name after switch `-receive` will put the program in the Client mode
Client will wait for a seeder to send `Hello.txt`
