# TODO: Should imports go on one line?
import socket
import json
import request_handler
import ssp_generator
from mdp import RTDP

IP_ADDRESS = '127.0.0.1'
PORT = 8000
GRAPH_FILE = 'graphs/generic-world-graph.json'

if __name__ == '__main__':
    print('Starting the planning service...')
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((IP_ADDRESS, PORT))
    socket.listen(1)

    print('Reading graph data...')
    with open(GRAPH_FILE) as file:
        graph = json.load(file)

    print("Generating SSP...")
    ssp = ssp_generator.generate(graph, 1, 5)

    print("Retrieving policy...")
    rtdp = RTDP(trials=5)
    policy = ssp.solve(solver=rtdp)

    print "Policy"
    print policy

    print('Waiting for a connection...')
    (connection, address) = socket.accept()

    print('Entering action loop...')
    while True:
        request = json.loads(connection.recv(1024))
        print('Received request: %s' % str(request))

        response = request_handler.handle(request)
        connection.sendall(response)
        print('Sent response: %s' % str(response))

    print('Closing the connection...')
    connection.close()

    print('Terminating the planning service...')
    socket.close()
