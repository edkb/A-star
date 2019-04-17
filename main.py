"""
Python implementation of the A* algorithm for the 8-Puzzle board game

Author: Eduardo K. Binotto

To execute this script run at the command-line: $ python3 main.py [F]

    To use just with uniform cost leave F blank

    To use the simplest heuristic use F = F1

    To use the mid-term heuristic F = F2

    To use the best heuristic F = F3

Requirements: Python 3.6+

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

        print(f'Execution time: {round((te - ts), 3)} seconds')
        return result
    return timed


initial_state = [
    [5, 6, 8],
    [3, 0, 1],
    [4, 2, 7]
]

final_state = [
   #  Column
   # 0  1  2
    [1, 2, 3],  # Line 0
    [4, 5, 6],  # Line 1
    [7, 8, 0]   # Line 2
]


class Node:
    """
    Represents a state of the board

    Also stores the associated cost for reaching that state,
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
        str_repr = '________\n'
        for line in self.state:
            str_repr += '|'
            for column in line:
                if column == 0:
                    column = ' '
                str_repr += (str(column) + ' ')
            str_repr += '|\n'
        str_repr += '‾‾‾‾‾‾‾‾\n'
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
        return self.cost + self.misplaced_tiles

    @property
    def f2(self):
        """
        Returns the cost to the node +
        how many numbers are wrong in columns and lines
        """
        return self.cost + self.misplaced_columns_and_lines

    @property
    def f3(self):
        """
        Return the cost to the node +
        the sum of all manhattan distances
        """
        return self.cost + self.manhattan_distance

    @property
    def misplaced_tiles(self):
        """
        Calculate hoy many numbers in the state
        are different from the goal state
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
    def misplaced_columns_and_lines(self):
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
    def manhattan_distance(self):
        """
        Calculates how many linear moves is necessary
        for each tile to reach the goal position
        :return: sum of all distances
        """

        total_distance = 0

        for n in range(1, 9):

            for line_number, line in enumerate(self.state):
                for column_number, number in enumerate(line):

                    if n == number:
                        l1 = line_number
                        c1 = column_number

                    if n == final_state[line_number][column_number]:
                        l2 = line_number
                        c2 = column_number

            horizontal_distance = abs(l2 - l1)
            vertical_distance = abs(c2 - c1)

            node_distance = horizontal_distance + vertical_distance
            total_distance += node_distance

        return total_distance

    @property
    def sons(self):
        """
        Iterates over the state and finds possible moves
        for the empty square. Each possible move is a new son
        :return: list of sons of the state
        """

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


def build_path(last_node):
    """
    Reconstructs the path from the final node up to
    the initial node by iterating over the nodes father

    :param last_node: The final node found by the algorithm
    :return: List of nodes forming the shortest path
             from the initial node to the goal
    """

    path = []

    # Iterates from the last node to the first one
    while last_node:
        # Inserts in the first position
        # in order to get the correct order
        path.insert(0, last_node)
        last_node = last_node.father

    # Prints the full path solution
    for n_move, move in enumerate(path):
        print(f'Move #{n_move}:')
        print(move)

    return path


def get_cost(current_node):
    return current_node.cost


def get_misplaced_tiles_heuristic(current_node):
    return current_node.f1


def get_misplaced_lines_and_columns_heuristic(current_node):
    return current_node.f2


def get_manhattan_heuristic(current_node):
    return current_node.f3


def loop(open_nodes, closed_nodes, frontier_length, current_cost, f):
    """
    Main algorithm loop

    Iterates over the frontier util it finds a path to the final state
    """

    while open_nodes:

        # Updates maximum frontier length
        if len(open_nodes) > frontier_length:
            frontier_length = len(open_nodes)

        # Sorts the open nodes list by node evaluation function value
        # with the lowest first (default list.sort() behavior)
        open_nodes.sort(key=f)

        # Get the lowest cost node and remove it
        # from the open nodes list
        current_node = open_nodes.pop(0)
        closed_nodes.add(current_node)

        # This is just for debugging and see if the algorithm
        # is really executing by printing each cost iteration
        if current_node.cost > current_cost:
            current_cost = current_node.cost
            print(f'Current cost: {current_cost}')

        # Checks whether the node state is the final state
        if current_node.state == final_state:
            print('\nWe made it!')

            moves = build_path(current_node)

            print(f'Visited nodes: {len(closed_nodes)}')
            print(f'Frontier length: {frontier_length}')
            print(f'Path size: {current_node.cost} ')

            return moves

        # This nested loops checks if the son of the
        # current node is already in the closed nodes list.
        # If it doesn't, add it to the open nodes list
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
        f = get_misplaced_tiles_heuristic

    elif mode == 'F2':
        print('Considering path cost and number of wrong tiles by lines and columns')
        f = get_misplaced_lines_and_columns_heuristic

    elif mode == 'F3':
        print('Considering path cost and total manhattan distance')
        f = get_manhattan_heuristic

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

    if sys.version_info < (3, 7):
        print(f"Please use python 3.6+. Your currently version is {sys.version[:3]}")
        sys.exit()

    strategy = None
    if len(sys.argv) > 1:
        strategy = sys.argv[1]

    shortest_path = a_star(strategy)
