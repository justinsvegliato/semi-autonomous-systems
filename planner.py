import socket
import json
import argparse
import graph_parser
import request_generator
from mdp import RTDP

SERVICE_IP_ADDRESS = '127.0.0.1'
SERVICE_PORT = 8002

parser = argparse.ArgumentParser(description='Control a vehicle in a simulated world.')
parser.add_argument('world', metavar='world', help='the file that contains the world')
parser.add_argument('start_state', metavar='start_state', type=int, help='the start state of the world')
parser.add_argument('goal_state', metavar='goal_state', type=int, help='the goal state of the world')
args = parser.parse_args()

graph_file = args.world
start_state = args.start_state
goal_state = args.goal_state

print('Reading graph data...')
with open(graph_file) as file:
    graph = json.load(file)

print('Generating SSP...')
ssp = graph_parser.get_ssp(graph, start_state, goal_state)

print('Retrieving policy...')
policy = ssp.solve(solver=RTDP())
print 'Policy: %s' % policy

print('Connecting to the simulator...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVICE_IP_ADDRESS, SERVICE_PORT))

current_state = start_state

print('Entering action loop...')
while current_state != goal_state:
    current_action = policy[current_state]

    next_state = current_action[1]
    next_action = policy[next_state]

    direction = graph_parser.get_turn(graph, current_action, next_action)

    request = request_generator.get_control_request(direction)
    server.sendall(request)
    print('Send control request: %s' % str(request))

    response = json.loads(server.recv(1024))
    print('Received response: %s' % str(response))

    if response[u'status'] == 'failure':
        print('Terminating the planner due to a failure...')
        break

    current_state = next_state

print('The simulator reached the goal state.')

print('Terminating the simulator...')
server.close()