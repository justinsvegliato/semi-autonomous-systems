import socket
import json
import argparse
import graph_parser
import request_generator
from mdp import RTDP

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 8002

def main():
    graph_file = args.world
    start_state = args.start_state
    goal_state = args.goal_state

    print('Reading the graph data...')
    with open(graph_file) as file:
        graph = json.load(file)

    print('Generating the SSP...')
    ssp = graph_parser.get_ssp(graph, start_state, goal_state)

    policy = ssp.solve(solver=RTDP())
    print 'Calculated the policy: %s' % policy

    print('Connecting to the simulator...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVICE_IP_ADDRESS, SERVICE_PORT))

    current_state = start_state
    print('Assigned the state state: %s' % current_state)

    print('Entering the drive loop...')
    while current_state != goal_state:
        current_action = policy[current_state]

        next_state = current_action[1]
        next_action = policy[next_state]

        direction = graph_parser.get_turn(graph, current_action, next_action)

        request = request_generator.get_control_request(direction)
        server.sendall(request)
        print('Sent a control request: %s' % request)

        response = json.loads(server.recv(1024))
        print('Received a response: %s' % response)

        if response['status'] == 'failure':
            print('Terminating the planner due to a failure...')
            break

        current_state = next_state

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