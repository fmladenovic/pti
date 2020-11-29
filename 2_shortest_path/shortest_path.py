# %% Define environment
import numpy as np
import matplotlib.pyplot as plt
# import networkx as nx
import math

from numpy.core.defchararray import index

# %%

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
H = 7
dictionary = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


# def show_graph(adjacency_matrix):
#     G = nx.from_numpy_matrix(np.matrix(adjacency_matrix), create_using=nx.DiGraph)
#     layout = nx.spring_layout(G)
#     nx.draw(G, layout)
#     labels = nx.get_edge_attributes(G, "weight")
#     nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
#     plt.show()

def print_path(path):
    to_print = ''
    for i in range(len(path)-1):
        to_print += dictionary[path[i]] + ' -> '

    to_print += dictionary[path[-1]]
    print(to_print)

def print_values(values):
    to_print = ''
    for (i, value) in enumerate(values):
        to_print += dictionary[i] + ' = ' + str(value) + '\n'
    print(to_print)


def non_zero_indexes(array):
    return np.nonzero(array)[0].tolist()

environment = [
    [0, 1, 1, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [0, 1, 0, 1, 0],
]

# show_graph(environment)
indexes = non_zero_indexes([0,0,1,0,1])
print(indexes)


# %%
# TASK 1

def calculate_state_values(environment, end):
    assert(0 < end and end <= len(environment), 'Idex out of bound!')

    v = [-math.inf if i != end else 0 for i in range(len(environment))]

    nodes_to_check = [end]

    while( len(nodes_to_check) != 0 ):
        current_node = nodes_to_check.pop()
        neighbors = non_zero_indexes(environment[current_node])
        
        for n in neighbors:
            new_value = v[current_node] - 1
            if new_value > v[n]:
                v[n] = new_value
                nodes_to_check.append(n)
    return v


def shortest_path(environment, start, end):
    assert(0 < end and end <= len(environment), 'END out of bound!')
    assert(0 < start and start <= len(environment), 'START out of bound!')

    state_values = calculate_state_values(environment, end)
    path = [start]
    current_node = start
    while( current_node != end ):
        possible_nodes = non_zero_indexes(environment[current_node])
        possible_nodes_values = np.take(state_values, possible_nodes)  # Get possible values
        current_node = possible_nodes[np.argmax( possible_nodes_values )] # Pick index of max value (node with max value)
                                                                          #  and step on that node
        path.append(current_node) # Add node
        # Do while you are not on terminate node
    return path

print_path(shortest_path(environment, A, E)) # A, B, E
print_path(shortest_path(environment, C, E)) # C, D, E
print_path(shortest_path(environment, B, E)) # B, E
print_path(shortest_path(environment, D, E)) # D, E


# %%
# Task 2

def generate_inverse_graph( graph ):
    inverse_graph = [ [0]*len(graph[0]) for _ in range( len(graph)) ]
    for (pointed_from, node) in enumerate(graph):
        point_to_nodes = non_zero_indexes(node)
        for pointed_node in point_to_nodes:
            inverse_graph[pointed_node][pointed_from] = node[pointed_node]
    return inverse_graph

test_env = [
    [0, 1, 1],
    [0, 0, 1],
    [0, 0, 0]
]

print(generate_inverse_graph( test_env )) # [[0, 0, 0], [1, 0, 0], [1, 1, 0]]

def dir_calculate_state_values(environment, end):
    assert(0 < end and end <= len(environment), 'Idex out of bound!')

    v = [-math.inf if i != end else 0 for i in range(len(environment))]
    inverse_environment = generate_inverse_graph(environment)

    nodes_to_check = [end]

    while( len(nodes_to_check) != 0 ):
        current_node = nodes_to_check.pop()
        neighbors = non_zero_indexes(inverse_environment[current_node])
        
        for n in neighbors:
            new_value = v[current_node] - 1
            if new_value > v[n]:
                v[n] = new_value
                nodes_to_check.append(n)
    return v


# %%
# Task 3

#    A  B  C  D  E  F  G
big_environment = [
    [0, 1, 1, 0, 0, 1, 0], # A
    [0, 0, 0, 1, 1, 1, 0], # B
    [0, 0, 0, 1, 0, 0, 1], # C
    [0, 0, 0, 0, 1, 0, 0], # D
    [0, 1, 0, 1, 0, 0, 0], # E
    [0, 1, 0, 0, 0, 0, 1], # F
    [0, 0, 1, 0, 0, 1, 0], # G
]

# show_graph(big_environment)


def calculate_state_values_for_multiple_terminal_nodes(environment, ends):
    assert(len(environment) != 0, 'You should add at least 1 state!')
    assert(len(ends) != 0, 'You should add at least 1 terminal state!')
    for end in ends:
        assert(0 < end and end <= len(environment), 'END out of bound!')
    
    inverse_environment = generate_inverse_graph(environment)
    v = [-math.inf if i not in ends else 0 for i in range(len(environment))]

    for end in ends:
        nodes_to_check = [end]

        while( len(nodes_to_check) != 0 ):
            current_node = nodes_to_check.pop()
            neighbors = non_zero_indexes(inverse_environment[current_node])
            
            for n in neighbors:
                new_value = v[current_node] - 1
                if new_value > v[n]:
                    v[n] = new_value
                    nodes_to_check.append(n)
    return v

values = calculate_state_values_for_multiple_terminal_nodes(big_environment, [E, G])
print_values(values)
# A = -2, B = -1, C = -1, D = -1, E = 0, F = -1, G = 0

def shortest_path_for_multiple_terminal_nodes(environment, start, ends):
    assert(len(environment) != 0, 'You should add at least 1 state!')
    assert(len(ends) != 0, 'You should add at least 1 terminal state!')
    for end in ends:
        assert(0 < end and end <= len(environment), 'END out of bound!')

    state_values = calculate_state_values_for_multiple_terminal_nodes(environment, ends)
    path = [start]
    current_node = start
    while( current_node not in ends ):
        possible_nodes = non_zero_indexes(environment[current_node])
        possible_nodes_values = np.take(state_values, possible_nodes)  # Get possible values
        current_node = possible_nodes[np.argmax( possible_nodes_values )] # Pick index of max value (node with max value)
                                                                          #  and step on that node
        path.append(current_node) # Add node
        # Do while you are not on terminate node
    return path

print_path(shortest_path_for_multiple_terminal_nodes(big_environment, A, [E, G])) # A, B, E
print_path(shortest_path_for_multiple_terminal_nodes(big_environment, B, [E, G])) # B, E
print_path(shortest_path_for_multiple_terminal_nodes(big_environment, F, [E, G])) # F, G
print_path(shortest_path_for_multiple_terminal_nodes(big_environment, C, [E, G])) # C, G


# %%
# Task 4


#    A  B  C  D  E  F  G
weighted_big_environment = [
    [0, 2, 1, 0, 0, 2, 0], # A
    [0, 0, 0, 2, 2, 2, 0], # B
    [0, 0, 0, 2, 0, 0, 2], # C
    [0, 0, 0, 0, 2, 0, 0], # D
    [0, 2, 0, 2, 0, 0, 0], # E
    [0, 2, 0, 0, 0, 0, 2], # F
    [0, 0, 2, 0, 0, 2, 0], # G
]

# show_graph(weighted_big_environment)



def weighted_calculate_state_values(environment, ends):
    assert(len(environment) != 0, 'You should add at least 1 state!')
    assert(len(ends) != 0, 'You should add at least 1 terminal state!')
    for end in ends:
        assert(0 < end and end <= len(environment), 'END out of bound!')
    
    inverse_environment = generate_inverse_graph(environment)
    v = [-math.inf if i not in ends else 0 for i in range(len(environment))]

    for end in ends:
        nodes_to_check = [end]

        while( len(nodes_to_check) != 0 ):
            current_node = nodes_to_check.pop()
            neighbors = non_zero_indexes(inverse_environment[current_node])

            for n in neighbors:
                new_value = v[current_node] - inverse_environment[current_node][n]
                if new_value > v[n]:
                    v[n] = new_value
                    nodes_to_check.append(n)
    return v

def weighted_shortest_path(environment, start, ends):
    assert(len(environment) != 0, 'You should add at least 1 state!')
    assert(len(ends) != 0, 'You should add at least 1 terminal state!')
    for end in ends:
        assert(0 < end and end <= len(environment), 'END out of bound!')

    state_values = weighted_calculate_state_values(environment, ends)
    path = [start]
    current_node = start
    while( current_node not in ends ):
        possible_nodes = non_zero_indexes(environment[current_node])
        possible_nodes_values = np.take(state_values, possible_nodes)  # Get possible values

        for (i, possible_node) in enumerate(possible_nodes): # Include transition price
            possible_nodes_values[i] -= environment[current_node][possible_node]

        current_node = possible_nodes[np.argmax( possible_nodes_values )] # Pick index of max value (node with max value)
                                                                          #  and step on that node
        path.append(current_node) # Add node
        # Do while you are not on terminate node
    return path

values = weighted_calculate_state_values(weighted_big_environment, [E, G])
print_values(values)

print_path(weighted_shortest_path(weighted_big_environment, A, [E, G])) # A, C, G
print_path(weighted_shortest_path(weighted_big_environment, F, [E, G])) # F, G
print_path(weighted_shortest_path(weighted_big_environment, B, [E, G])) # B, E
print_path(weighted_shortest_path(weighted_big_environment, D, [E, G])) # D, E



# %%