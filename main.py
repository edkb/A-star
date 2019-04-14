"""
PYthon A* implementation

Antonio Gomes and Eduardo Binotto
"""

import copy


class Node:

    def __init__(self, state, cost=0, father=None):

        self.state = state
        self.cost = cost
        self.sons = []
        self.father = father

    def __str__(self):
        str_repr = '-----\n'
        for line in self.state:
            for column in line:
                str_repr += (str(column) + ' ')
            str_repr += '\n'
        str_repr += '-----\n'
        return str_repr

    @property
    def f1(self):
        return self.cost + self.get_simple_heuristics()

    def get_simple_heuristics(self):

        wrong_numbers = 0

        for line_number, line in enumerate(self.state):
            for column_number, number in enumerate(line):

                correct_number = final_state[line_number][column_number]

                if number != correct_number:
                    wrong_numbers += 1

        return wrong_numbers

    def get_node_sons(self):

        sons = []

        for line_number, line in enumerate(self.state):
            for column_number, number in enumerate(line):

                # If is the square
                if number == 0:

                    # Square can go up
                    if line_number > 0:
                        new_son = copy.deepcopy(self.state)

                        # Get the number of the up position
                        flip_number = self.state[line_number - 1][column_number]

                        # Set the number of the up position to 0
                        new_son[line_number - 1][column_number] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        sons.append(
                            Node(state=new_son, cost=self.cost+1, father=self)
                        )

                    # Square can go down
                    if line_number < 2:
                        new_son = copy.deepcopy(self.state)

                        # Get the number of the down position
                        flip_number = self.state[line_number + 1][column_number]

                        # Set the number of the down position to 0
                        new_son[line_number + 1][column_number] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        sons.append(
                            Node(state=new_son, cost=self.cost+1, father=self)
                        )

                    # Square can go right
                    if column_number < 2:
                        new_son = copy.deepcopy(self.state)

                        # Get the number of the right position
                        flip_number = self.state[line_number][column_number + 1]

                        # Set the number of the right position to 0
                        new_son[line_number][column_number + 1] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        sons.append(
                            Node(state=new_son, cost=self.cost+1, father=self)
                        )

                    # Square can go left
                    if column_number > 0:
                        new_son = copy.deepcopy(self.state)

                        # Get the number of the left position
                        flip_number = self.state[line_number][column_number - 1]

                        # Set the number of the left position to 0
                        new_son[line_number][column_number - 1] = 0

                        # Set the current 0 position to the flip number
                        new_son[line_number][column_number] = flip_number

                        sons.append(
                            Node(state=new_son, cost=self.cost+1, father=self)
                        )
        return sons

    def print_sons(self):
        for sun_number, son in enumerate(self.sons):
            print(f'Son #{sun_number}')
            print(son)


def build_path(last_node):
    """
    Reconstructs the path from the final node up to
    the initial node by iterating over the nodes father

    :param last_node: The final node found by the algorithm
    :return: List of nodes forming the shortest path
             from the initial node to the goal
    """
    path = []
    while last_node:
        path.insert(0, last_node)
        last_node = last_node.father
    return path


def get_cost(current_node):
    return current_node.cost


def get_heuristic(current_node):
    return current_node.f1


final_state = [
   #  Column
   # 0  1  2
    [1, 2, 3],  # Line 0
    [4, 5, 6],  # Line 1
    [7, 8, 0]   # Line 2
]

initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]


def a_star(mode='C'):
    """
    Main search algorithm

    Finds the best possible path between any
    initial board state and the final state

    :param mode: Define the sorting strategy
    :return: list of nodes containing board states
    """

    # By default we use just the cost
    # as our sorting strategy
    f = get_cost

    if mode == 'F1':
        f = get_heuristic

    first_node = Node(initial_state)
    current_cost = first_node.cost

    # The python data type list is used to store
    # the open nodes because we need to rely on the
    # cost and heuristic values to get the most
    # promising results and lists are easy to store
    # and sort data in this way
    open_nodes = [first_node]

    # The set data structure is used because
    # its a lightweight way to store unordered
    # and unrepeated peaces of data (our nodes)
    closed_nodes = set()

    while open_nodes:

        # Sorts the open nodes list by node cost
        # with the lowest cost first
        open_nodes.sort(key=f)

        # Get the lowest cost node and remove it from
        # the open nodes list
        current_node = open_nodes.pop(0)
        closed_nodes.add(current_node)

        if current_node.state == final_state:
            print('\nWe made it!')
            print(f'Visited nodes: {len(closed_nodes)}')
            print(f'Path size: {current_node.cost} ')

            return build_path(current_node)

        if current_node.cost > current_cost:
            # Just for debugging
            current_cost = current_node.cost
            print(f'Current cost: {current_cost}')

        sons = current_node.get_node_sons()

        # This nested loops checks if the son of the
        # current node is already in the closed nodes list.
        # If doesn't, add it to the open nodes list
        for son in sons:
            for visited in closed_nodes:
                if son.state == visited.state:
                    break
            else:
                open_nodes.append(son)


if __name__ == '__main__':

    uniform_cost = a_star()

    simple_heuristics = a_star('F1')
