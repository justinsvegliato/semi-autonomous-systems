import socket
import json
import request_generator
import graph_parser
from mdp import RTDP

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 8000

GRAPH_FILE = 'graphs/example-graph-1.json'
START_STATE = 1
GOAL_STATE = 5

def main():
    print('Reading graph data...')
    with open(GRAPH_FILE) as file:
        graph = json.load(file)

    print("Generating SSP...")
    ssp = graph_parser.get_ssp(graph, START_STATE, GOAL_STATE)

    print("Retrieving policy...")
    policy = ssp.solve(solver=RTDP())
    print "Policy: %s" % policy

    print('Connecting to the simulator...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVICE_IP_ADDRESS, SERVICE_PORT))

    print('Entering action loop...')
    while True:
        print('Sending location request...')
        request = request_generator.get_location_request()
        server.sendall(request)
        response = socket.recv(1024)

        coordinates = (response.x, response.y, response.z)
        state = graph_parser.get_state(graph, ssp, coordinates)
        action = policy[state]
        direction = action

        print('Sending control request...')
        request = request_generator.get_control_request(direction)
        server.sendall(request)
        response = socket.recv(1024)

    print('Terminating the simulator...')
    socket.close()

if __name__ == '__main__':
    main()