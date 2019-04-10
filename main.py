"""
PYthon A* implementation

Antonio Gomes and Eduardo Binotto
"""


def reconstruct_path(came_from, current):

    total_path = current

    while current in came_from.keys():

        current = came_from[current]
        total_path.append(current)

    return total_path


def get_heuristic(current_node):
    return 10


def distance_between(current_node, neighbor):
    return 20


def a_star(initial_state, final_state):
    """
    Main algorithm
    :return:
    """

    closed_nodes = []
    open_nodes = list()
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

        for neighbor in current_node:

            if neighbor in closed_nodes:
                continue

            current_score = path_cost[current_node] + distance_between(current_node, neighbor)

            if neighbor not in open_nodes:
                open_nodes.append(neighbor)
                open_nodes.sort()

            elif current_score >= path_cost[neighbor]:
                continue

        came_from[neighbor] = current_node
        path_cost[neighbor] = current_score
        total_cost = path_cost[current_node] + distance_between(neighbor, final_state)
