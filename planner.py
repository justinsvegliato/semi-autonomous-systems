import socket
import json
import request_generator
import graph_parser
from mdp import RTDP

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 8002

GRAPH_FILE = 'graphs/example-graph-1.json'
START_STATE = 1
GOAL_STATE = 5

def main():
    print('Reading graph data...')
    with open(GRAPH_FILE) as file:
        graph = json.load(file)

    print('Generating SSP...')
    ssp = graph_parser.get_ssp(graph, START_STATE, GOAL_STATE)

    print('Retrieving policy...')
    policy = ssp.solve(solver=RTDP())
    print 'Policy: %s' % policy

    print('Connecting to the simulator...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVICE_IP_ADDRESS, SERVICE_PORT))

    current_state = START_STATE

    print('Entering action loop...')
    while current_state != GOAL_STATE:
        action = policy[current_state]
        direction = graph_parser.get_turn(graph, action)
        request = request_generator.get_control_request(direction)    
        server.sendall(request)
        print('Send control request: %s' % str(request))

        response = json.loads(server.recv(1024))
        print('Received response: %s' % str(response))

        if response[u'status'] == 'failure':
            print('Terminating the planner due to a failure...')
            break

        current_state = action[1]

    print('The simulator reached the goal state!')

    print('Terminating the simulator...')
    server.close()

if __name__ == '__main__':
    main()