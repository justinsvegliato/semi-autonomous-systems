import socket
import json

IP_ADDRESS = '127.0.0.1'
PORT = 8002

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

        response = json.dumps({'id': request['id'], 'status': 'success'})
        connection.sendall(response)
        print('Sent response: %s' % response)

    print('Closing the connection...')
    connection.close()

    print('Terminating the simulator...')
    server.close()

if __name__ == '__main__':
    main()