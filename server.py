import random
import socket

IP = '127.0.0.1'
PORT = 5010

LEFT = -1
STRAIGHT = 0
RIGHT = 1
ACTIONS = [LEFT, STRAIGHT, RIGHT] 

if __name__ == '__main__':
    print('Starting server...')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP, PORT))

    action = 0
    is_active = True 

    while is_active:
        print('Waiting for connection...')
        response = sock.recvfrom(1024)
        data = response[0]
        client_address = response[1]
        
        text = str(data)
        text = text.split("\\")[0]
        text = text[2:len(text)]
        text = text.rstrip('\n')
        print('Received response: %s' % text)
        
        if text is 'action':
            action = random.choice(ACTIONS) 
            sock.sendto(bytearray('%d\0' % action, 'utf-8'), client_address)

        if text is 'stop':
            is_active = False 
            sock.sendto(bytearray('Stopping...', 'utf-8'), client_address)

    print('Terminating server...')
    sock.close()

