# TODO: Clean up unicode attributes
# TODO: Rename to firstNodeId and secondNodeId since bidirectional roads are implied
import numpy as np
from mdp import SSP
import direction_calculator

def get_ssp(graph, start_state, goal_state):
    states = get_states(graph)
    get_actions = get_action_function(graph, states)
    get_transition_probabilities = get_transition_function(states, get_actions)
    get_cost = get_cost_function(graph, states, get_actions, goal_state)

    return SSP(
        states,
        get_actions,
        get_transition_probabilities,
        get_cost,
        get_key,
        start_state,
        goal_state
    )

def get_turn(graph, current_action, next_action):
    current_start_node = get_node(graph, current_action[0])
    current_end_node = get_node(graph, current_action[1])
    next_start_node = get_node(graph, next_action[0])
    next_end_node = get_node(graph, next_action[1])

    current_start_vector = (current_start_node[u'x'], current_start_node[u'y'])
    current_end_vector = (current_end_node[u'x'], current_end_node[u'y'])
    next_start_vector = (next_start_node[u'x'], next_start_node[u'y'])
    next_end_vector = (next_end_node[u'x'], next_end_node[u'y'])

    current_direction_vector = np.subtract(current_start_vector, current_end_vector)
    next_direction_vector = np.subtract(next_start_vector, next_end_vector)

    return direction_calculator.get_turn(next_direction_vector, current_direction_vector)

def get_states(graph):
    return [node[u'id'] for node in graph[u'nodes']]

def get_action_function(graph, states):
    state_action_map = {}
    for state in states:
        state_action_map[state] = []
        for edge in graph[u'edges']:
            first_node_id = edge[u'startNodeId']
            second_node_id = edge[u'endNodeId']
            if state == first_node_id:
                state_action_map[state].append((first_node_id, second_node_id))
            elif state == second_node_id:
                state_action_map[state].append((second_node_id, first_node_id))

    def get_actions(state):
        return state_action_map[state]

    return get_actions

def get_transition_function(states, get_actions):
    transition_probabilities = {}
    for state in states:
        transition_probabilities[state] = {}
        for action in get_actions(state):
            transition_probabilities[state][action] = [(action[1], 1)]

    def get_transition_probabilities(state, action):
        return transition_probabilities[state][action]

    return get_transition_probabilities

def get_cost_function(graph, states, get_actions, goal_state):
    costs = {}
    for state in states:
        costs[state] = {}
        for action in get_actions(state):
            for edge in graph[u'edges']:
                first_node_id = edge[u'startNodeId']
                second_node_id = edge[u'endNodeId']
                if action[0] == first_node_id and action[1] == second_node_id or action[0] == second_node_id and action[1] == first_node_id:
                    costs[state][action] = edge[u'weight'] if state != goal_state else 0

    def get_cost(state, action):
        return costs[state][action]

    return get_cost

def get_node(graph, id):
    for node in graph[u'nodes']:
        if id == node[u'id']:
            return node
    return None

def get_key(state):
    return state