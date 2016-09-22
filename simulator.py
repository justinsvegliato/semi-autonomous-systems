import socket
import json
import time

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 8000

if __name__ == '__main__':
    print('Starting the simulator...')

    print('Connecting to the planning service...')
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((SERVICE_IP_ADDRESS, SERVICE_PORT))

    while True:
        print('Sending a request...')
        request = json.dumps({
            'type': 'action',
            'data': {
                'x': 1,
                'y': 2,
                'z': 3
            }
        })
        socket.sendall(request)

        time.sleep(5)

    print('Terminating the simulator...')
    socket.close()

