# TODO: Clean up unicode attributes
# TODO: Rename to firstNodeId and secondNodeId since bidirectional roads are implied
from mdp import SSP

def generate(graph, start_state, goal_state):
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

def get_key(state):
    return state