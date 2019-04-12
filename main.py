"""
PYthon A* implementation

Antonio Gomes and Eduardo Binotto
"""

import copy


class Node:

    def __init__(self, state):

        self.state = state
        self.sons = []

    def __str__(self):
        str_repr = '-----\n'
        for line in self.state:
            for column in line:
                str_repr += (str(column) + ' ')
            str_repr += '\n'
        str_repr += '-----\n'
        return str_repr

    def get_node_sons(self):
        current_node = self.state

        for line_number, line in enumerate(current_node):
            for column_number, number in enumerate(line):

                # If is the square
                if number == 0:

                    print(f'0 at line {line_number} and column {column_number}')

                    # Square can go up
                    if line_number > 0:
                        new_son = copy.deepcopy(current_node)

                        # Get the number of the up position
                        flip_number = current_node[line_number - 1][column_number]

                        # Set the number of the up position to 0
                        new_son[line_number - 1][column_number] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        self.sons.append(Node(new_son))

                    # Square can go down
                    if line_number < 2:
                        new_son = copy.deepcopy(current_node)

                        # Get the number of the down position
                        flip_number = current_node[line_number + 1][column_number]

                        # Set the number of the down position to 0
                        new_son[line_number + 1][column_number] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        self.sons.append(Node(new_son))

                    # Square can go right
                    if column_number < 2:
                        new_son = copy.deepcopy(current_node)

                        # Get the number of the right position
                        flip_number = current_node[line_number][column_number + 1]

                        # Set the number of the right position to 0
                        new_son[line_number][column_number + 1] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        self.sons.append(Node(new_son))

                    # Square can go left
                    if column_number > 0:
                        new_son = copy.deepcopy(current_node)

                        # Get the number of the left position
                        flip_number = current_node[line_number][column_number - 1]

                        # Set the number of the left position to 0
                        new_son[line_number][column_number - 1] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        self.sons.append(Node(new_son))

    def print_sons(self):
        for sun_number, son in enumerate(self.sons):
            print(f'Son #{sun_number}')
            print(son)


def reconstruct_path(came_from, current):

    total_path = current

    while current in came_from.keys():

        current = came_from[current]
        total_path.append(current)

    return total_path


def get_heuristic(current_node):
    return 10


def distance_between(current_node, son):
    return 20


final_state = [
   #  Column
   # 0  1  2
    [1, 3, 3],  # Line 0
    [6, 5, 4],  # Line 1
    [7, 8, 0]   # Line 2
]

initial_state = [
    [2, 3, 5],
    [8, 0, 7],
    [1, 4, 6]
]


def a_star():
    """
    Main algorithm
    :return:
    """

    closed_nodes = []
    open_nodes = []

    # Add the starting node to the open nodes list
    open_nodes.append(initial_state)

    came_from = {}

    path_cost = {'start': 0}
    total_cost = path_cost['start'] + get_heuristic('start')

    while open_nodes:

        open_nodes.sort()
        current_node = open_nodes[0]

        if current_node == final_state:
            return reconstruct_path(came_from, current_node)

        open_nodes.remove(current_node)
        closed_nodes.append(current_node)

        sons = get_node_sons(current_node)

        for son in sons:

            if son in closed_nodes:
                continue

            current_score = path_cost[current_node] + distance_between(current_node, son)

            if son not in open_nodes:
                open_nodes.append(son)
                open_nodes.sort()

            elif current_score >= path_cost[son]:
                continue

        came_from[son] = current_node
        path_cost[son] = current_score
        total_cost = path_cost[current_node] + distance_between(son, final_state)
