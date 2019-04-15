"""
Python A* implementation

Antonio Gomes and Eduardo Binotto
"""

import sys
import copy
import time


def timeit(method):
    """
    Measures any method execution time
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print(f'Execution time: {round((te - ts), 2)} seconds')
        return result

    return timed


class Node:
    """
    Represents a state of the board

    Also stores de cost associated for reaching that state,
    and the immediate node that led to that state
    """

    def __init__(self, state, cost=0, father=None):

        self._state = state
        self.cost = cost
        self.father = father

    def __str__(self):
        """
        Prettily prints state to the console
        :return: string representation of the state
        """
        str_repr = '-----\n'
        for line in self.state:
            for column in line:
                str_repr += (str(column) + ' ')
            str_repr += '\n'
        str_repr += '-----\n'
        return str_repr

    @property
    def state(self):
        return self._state

    @property
    def f1(self):
        """
        Returns the cost to the node +
        the value of the simple heuristic strategy
        """
        return self.cost + self.simple_heuristics

    @property
    def f2(self):
        """
        Returns the cost to the node +
        how many numbers are wring in columns and lines
        """
        return self.cost + self.wrong_columns_and_lines

    @property
    def simple_heuristics(self):
        """
        Calculate hoy many numbers in the state are different from the goal state
        :return: wrong number units
        """

        wrong_numbers = 0

        for line_number, line in enumerate(self.state):
            for column_number, number in enumerate(line):

                correct_number = final_state[line_number][column_number]

                if number != correct_number:
                    wrong_numbers += 1

        return wrong_numbers

    @property
    def wrong_columns_and_lines(self):
        """
        Iterates over board lines and columns to find misplaced numbers

        :return: How many numbers have wrong columns +
                 how many numbers have wrong lines
        """

        wrong_numbers = 0

        # Create a copy of the state for the transpose operation
        state = copy.deepcopy(self.state)

        # Flip lines and columns (matrix transpose)
        t_state = list(zip(*state))

        for n in range(1, 9):

            for line_number, line in enumerate(self.state):
                for column_number, number in enumerate(line):

                    correct_number = final_state[line_number][column_number]

                    if correct_number == n:
                        l_n = line_number
                        c_n = column_number
                        break

            for li, line in enumerate(self.state):
                if l_n == li and n not in line:
                    wrong_numbers += 1
                    break

            for ci, column in enumerate(t_state):

                if c_n == ci and n not in column:
                    wrong_numbers += 1
                    break

        return wrong_numbers

    @property
    def best_heuristics(self):
        return None

    @property
    def sons(self):

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

    for move in path:
        print(move)

    return path


def get_cost(current_node):
    return current_node.cost


def get_heuristic(current_node):
    return current_node.f1


def get_lines_heuristic(current_node):
    return current_node.f2


final_state = [
   #  Column
   # 0  1  2
    [1, 2, 3],  # Line 0
    [4, 5, 6],  # Line 1
    [7, 8, 0]   # Line 2
]

initial_state = [
    [5, 6, 8],
    [3, 0, 1],
    [4, 2, 7]
]


def loop(open_nodes, closed_nodes, frontier_length, current_cost, f):
    """
    Main algorithm loop

    Iterates over the frontier util it finds a path to the final state

    :param open_nodes:
    :param closed_nodes:
    :param frontier_length:
    :param current_cost:
    :param f:
    :return: list of nodes from the initial to the final state
    """

    while open_nodes:

        if len(open_nodes) > frontier_length:
            frontier_length = len(open_nodes)

        # Sorts the open nodes list by node cost
        # with the lowest cost first
        open_nodes.sort(key=f)

        # Get the lowest cost node and remove it from
        # the open nodes list
        current_node = open_nodes.pop(0)
        closed_nodes.add(current_node)

        if current_node.cost > current_cost:
            # Just for debugging
            current_cost = current_node.cost
            print(f'Current cost: {current_cost}')

        if current_node.state == final_state:
            print('\nWe made it!')

            moves = build_path(current_node)

            print(f'Visited nodes: {len(closed_nodes)}')
            print(f'Frontier length: {frontier_length}')
            print(f'Path size: {current_node.cost} ')

            return moves

        # This nested loops checks if the son of the
        # current node is already in the closed nodes list.
        # If doesn't, add it to the open nodes list
        for son in current_node.sons:
            for visited in closed_nodes:
                if son.state == visited.state:
                    break
            else:
                open_nodes.append(son)


@timeit
def a_star(mode=None):
    """
    Main search algorithm

    Finds the best possible path between any
    initial board state and the final state

    :param mode: Define the sorting strategy
    :return: list of nodes containing board states
    """

    # By default we use just the cost
    # as our sorting strategy

    if not mode:
        f = get_cost
        print('Considering just path cost')

    elif mode == 'F1':
        print('Considering path cost and number of wrong tiles')
        f = get_heuristic

    elif mode == 'F2':
        print('Considering path cost and number of wrong tiles by lines and columns')
        f = get_lines_heuristic

    else:
        print('Wrong strategy input. Exiting')
        return

    first_node = Node(initial_state)
    current_cost = first_node.cost

    # The python data type list is used to store
    # the open nodes because we need to rely on the
    # cost and heuristic values to get the most
    # promising results and lists are easy to store
    # and sort data in this way
    open_nodes = [first_node]

    frontier_length = len(open_nodes)

    # The set data structure is used because
    # its a lightweight way to store unordered
    # and unrepeated peaces of data (our nodes)
    closed_nodes = set()

    return loop(open_nodes, closed_nodes, frontier_length, current_cost, f)


if __name__ == '__main__':

    strategy = None
    if len(sys.argv) > 1:
        strategy = sys.argv[1]

    shortest_path = a_star(strategy)
