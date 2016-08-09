import ctypes
import random
import server
import socket
import string
import threading
import time

class ActionSelector(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        
    def run(self):
        global action
            
        print('Starting thread...')       
        
        while True:
            lock.acquire()
            
            if not is_active:
                lock.release()
                break 
                
            action = random.randint(-1, 1)
            print('New action: %d' % action)
            
            lock.release()
            time.sleep(5.0)
            
        print('Stopping thread...')

lock = threading.Lock()
action = 0

if __name__ == '__main__':
    thread = ActionSelector(1, 'Action-Selector')
    thread.start()

    UDP_IP = '127.0.0.1'
    UDP_PORT = 5010

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, UDP_PORT))

    while is_active:
        response = sock.recvfrom(1024)
        data = response[0]
        client_address = response[1]
        
        text = str(data)
        text = text.split("\\")[0]
        text = text[2:len(text)]
        text = text.rstrip('\n')
        
        print('Response: %s' % text)
        
        if text is 'action':
            lock.acquire()
            print('Requested action...')
            # TODO Do some work here
            lock.release()
            
            action = 0
            sock.sendto(bytearray('%d\0' % action, 'utf-8'), client_address)
            
        if text is 'stop':
            lock.acquire()
            is_active = True
            lock.release()
            
            sock.sendto(bytearray('Stopping...', 'utf-8'), client_address)

    sock.close()

