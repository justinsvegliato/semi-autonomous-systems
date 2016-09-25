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

def get_direction_vector(graph, action):
    start_node = get_node(graph, action[0])
    start_vector = (start_node['x'], start_node['y'])

    end_node = get_node(graph, action[1])
    end_vector = (end_node['x'], end_node['y'])

    return np.subtract(start_vector, end_vector)

def get_turn(graph, current_action, next_action):
    current_direction_vector = get_direction_vector(graph, current_action)
    next_direction_vector = get_direction_vector(graph, next_action)
    return direction_calculator.get_turn(next_direction_vector, current_direction_vector)

def get_states(graph):
    return [node['id'] for node in graph['nodes']]

def get_action_function(graph, states):
    state_action_map = {}
    for state in states:
        state_action_map[state] = []
        for edge in graph['edges']:
            first_node_id = edge['firstNodeId']
            second_node_id = edge['secondNodeId']
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
            for edge in graph['edges']:
                first_node_id = edge['firstNodeId']
                second_node_id = edge['secondNodeId']
                if action[0] == first_node_id and action[1] == second_node_id or action[0] == second_node_id and action[1] == first_node_id:
                    costs[state][action] = edge['weight'] if state != goal_state else 0

    def get_cost(state, action):
        return costs[state][action]

    return get_cost

def get_node(graph, id):
    for node in graph['nodes']:
        if id == node['id']:
            return node
    return None

def get_key(state):
    return state