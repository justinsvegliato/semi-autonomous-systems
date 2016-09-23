import socket
import json

IP_ADDRESS = '127.0.0.1'
PORT = 8000

def main():
    print('Starting the simulator...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_ADDRESS, PORT))
    server.listen(1)

    print('Waiting for a connection...')
    (connection, ip_address) = server.accept()

    while True:
        request = json.loads(connection.recv(1024))
        print('Received request: %s' % str(request))

    print('Closing the connection...')
    connection.close()

    print('Terminating the simulator...')
    server.close()

if __name__ == '__main__':
    main()