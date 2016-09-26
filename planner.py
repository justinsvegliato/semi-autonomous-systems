#!/usr/bin/env python
import socket
import json
import argparse
import graph_parser
#from mdp import RTDP

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 8003

def main():
    graph_file = args.world
    start_state = args.start_state
    goal_state = args.goal_state

    print('Reading the graph data...')
    with open(graph_file) as file:
        graph = json.load(file)

    #print('Generating the SSP...')
    #ssp = graph_parser.get_ssp(graph, start_state, goal_state)

    # policy = ssp.solve(solver=RTDP())
    policy = {0: (0, 1), 1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 5), 5: (5, 6), 6: (6, 7), 7: (7, 8), 8: (8, 9), 9: (9, 10), 10: (10, 9)}
    print 'Calculated the policy: %s' % policy

    print('Connecting to the simulator...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVICE_IP_ADDRESS, SERVICE_PORT))

    current_state = None

    print('Entering the driving loop...')
    while current_state != goal_state:
        location = json.loads(server.recv(1024))

        if current_state is None or graph_parser.has_turned(graph, current_action, next_action, location['x'], location['y']):
            current_state = start_state if current_state is None else next_state
            current_action = policy[current_state]

            next_state = current_action[1]
            next_action = policy[next_state]

            direction = graph_parser.get_turn(graph, current_action, next_action)

            server.sendall(direction)
            print('Sent direction: %s' % direction)

    print('Reached the goal state: %s' % goal_state)

    print('Terminating the simulator...')
    server.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control a vehicle in a simulated world.')
    parser.add_argument('world', metavar='world', help='the file that contains the world')
    parser.add_argument('start_state', metavar='start_state', type=int, help='the start state of the world')
    parser.add_argument('goal_state', metavar='goal_state', type=int, help='the goal state of the world')
    args = parser.parse_args()

    main()
