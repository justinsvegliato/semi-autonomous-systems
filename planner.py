import socket
import json
import argparse
import graph_parser

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 5010

MARGIN = 5
DISTANCE_THRESHOLD = 20


def main():
    graph_file = 'graphs/example-graph.json'  # args.world
    start_state = 1  # args.start_state
    goal_state = 15  # args.goal_state

    print('Reading the graph data...')
    with open(graph_file) as file:
        graph = json.load(file)

    # print('Generating the SSP...')
    # ssp = graph_parser.get_ssp(graph, start_state, goal_state)

    # policy = ssp.solve(solver=RTDP())
    policy = {0: (0, 1), 1: (1, 2), 2: (2, 3), 3: (3, 4), 4: (4, 7), 7: (7, 9), 9: (9, 10), 10: (10, 11), 11: (11, 12), 12: (12, 13), 13: (13, 14), 14: (14, 15), 15: (15, 14)}
    print('Calculated the policy: %s' % policy)

    print('Creating the socket...')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVICE_IP_ADDRESS, SERVICE_PORT))

    total_distance = float('inf')
    step_distance = float('inf')

    current_state = None
    next_state = None

    print('Entering the driving loop...')
    while total_distance > DISTANCE_THRESHOLD:
        print('Waiting to receive a response from the simulator...')
        response = server.recvfrom(1024)
        data = response[0]
        client_address = response[1]

        text = str(data)
        text = text.split('\\')[0]
        text = text[2:len(text)]
        text = text.rstrip('\n')
        
        components = text.split(',')
        x = float(components[1]) 
        y = -float(components[0])
        location = (x, y)

        if current_state is None or step_distance + MARGIN < graph_parser.get_distance(graph, next_state, location):
            print('Calculating next direction...')
            current_state = start_state if current_state is None else next_state
            current_action = policy[current_state]

            next_state = current_action[1]
            next_action = policy[next_state]

            direction = graph_parser.get_turn(graph, current_action, next_action)

        total_distance = graph_parser.get_distance(graph, goal_state, location)
        step_distance = graph_parser.get_distance(graph, next_state, location)

        server.sendto(bytearray('%d\0' % direction, 'utf-8'), client_address)

        print('Current Location: (%f, %f)' % location)
        print('Total Distance: ', total_distance)
        print('Step Distance: ', step_distance)
        print('Current State:', current_state)
        print('Next State:', next_state)
        print('Direction:', direction)

    print('Reached the goal state: %s' % goal_state)

    print('Terminating the socket...')
    server.close()

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Control a vehicle in a simulated world.')
    # parser.add_argument('world', metavar='world', help='the file that contains the world')
    # parser.add_argument('start_state', metavar='start_state', type=int, help='the start state of the world')
    # parser.add_argument('goal_state', metavar='goal_state', type=int, help='the goal state of the world')
    # args = parser.parse_args()

    main()
