#!/usr/bin/env python
import socket
import json
import time

IP_ADDRESS = '127.0.0.1'
PORT = 8003

def main():
    print('Starting the simulator...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_ADDRESS, PORT))
    server.listen(1)

    print('Waiting for a connection...')
    (connection, ip_address) = server.accept()

    while True:
        location = json.dumps({'x': 5, 'y': 3});
        connection.sendall(location)
        print('Sent location: %s' % location)

        time.sleep(1)

    print('Closing the connection...')
    connection.close()

    print('Terminating the simulator...')
    server.close()

if __name__ == '__main__':
    main()