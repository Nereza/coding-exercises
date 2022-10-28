import math

# Relevant characters in the labyrinth input
AIR = '.'
START = 'S'
END = 'E'


def input_to_matrix(filename):
    """
    Transforms the input of multiple 3D labyrinths from a txt file to a list of labyrinths represented as matrices.
    Input:
    The first line of each labyrinth contains three non-negative integer values <= 30, seperated by one space:
        - L: number of layers
        - R: length of each layer
        - C: width of each layer
    The following lines describe the L layers of the labyrinth containing each R lines with C characters.
    Each character represents a square in the labyrinth:
        - '#' = rock, can' pass through
        - '.' = air, can pass through
        - 'S' = starting position
        - 'E' = end/destination position
    Each layer is followed by an empty line. The input is completed with a line of '0 0 0'.

    :param filename: txt file containing multiple 3D labyrinths
    :return: a list of labyrinth matrices from the input file.
    """
    labyrinths = []

    with open(filename, 'r') as file:
        lines = [line.rstrip() for line in file]

    for i in range(len(lines)):
        line = lines[i]
        if line:
            if line[0].isdigit() and line[0] != '0':   # start of a labyrinth
                depth, length, width = [int(char) for char in line.split()]

                L = []
                layer_start_line = i+1
                for d in range(depth):
                    L.append([])
                    for l in range(length):
                        line_index = layer_start_line+l
                        L[d].append(lines[line_index])
                    layer_start_line += length + 1      # +1 for empty line
                labyrinths.append(L)
    return labyrinths


def get_air_coordinates(labyrinth_matrix):
    """
    Always starts with the coordinates of the START square and ends with the coordinates of the END square.
    Coordinate [y, x, z] with
        - y: layer index
        - x: length index
        - z: width index
    :param labyrinth_matrix: the matrix of a single labyrinth, as created input_to_matrix
    :return: a list of coordinates of every air square of the given labyrinth, starting with the ones of START and ending with the ones of END
    """
    air_coordinates = []
    start = []
    end = []
    for y in range(len(labyrinth_matrix)):
        for x in range(len(labyrinth_matrix[y])):
            for z in range(len(labyrinth_matrix[y][x])):
                element = labyrinth_matrix[y][x][z]
                if element == AIR:
                    air_coordinates.append([y, x, z])
                if element == START:
                    start = [y, x, z]
                if element == END:
                    end = [y, x, z]
    air_coordinates = [start] + air_coordinates + [end]
    return air_coordinates


def is_adjacent(from_coord, to_coord):
    """
    Check whether two 3D coordinates are adjacent or not
    :param from_coord: 3D coordinate
    :param to_coord: 3D coordinate
    :return: True, if the coordinates are adjacent (not diagonally), otherwise False
    """
    connected = False
    diff_y = from_coord[0] - to_coord[0]
    diff_x = from_coord[1] - to_coord[1]
    diff_z = from_coord[2] - to_coord[2]
    if abs(diff_y) + abs(diff_x) + abs(diff_z) == 1:
        connected = True
    return connected


def to_graph(coordinates):
    """
    Transforms a list of 3D coordinates to a graph represented as list of adjacent sets
    :param coordinates: list of 3D coordinates [y, x, z]
    :return: graph as list of adjacent sets
    """
    length = len(coordinates)
    graph = [set() for _ in range(length)]

    for i in range(length):
        for j in range(length):
            if is_adjacent(coordinates[i], coordinates[j]):
                graph[i].add(j)

    return graph


def shortest_path(graph, start, end):
    """
    Calculates the shortest distance between the start and end vertex of a given graph based on Dijstra's algorithm.
    :param graph: graph represented as list of adjacent sets
    :param start: starting vertex
    :param end: destination vertex
    :return: shortest distance from start to end, if a path exists. Math.inf otherwise.
    """
    number_of_nodes = len(graph)
    distances = [math.inf]*number_of_nodes
    distances[start] = 0

    queue = {u for u in range(number_of_nodes)}

    while queue:
        (d, v) = min({(distances[u], u) for u in queue})
        if v == end or d == math.inf:
            break
        queue.remove(v)
        for u in graph[v]:
            alt = distances[v] + 1
            if distances[u] == math.inf or alt < distances[u]:
                distances[u] = alt

    return distances[end]


def escape_labyrinths(input_filename):
    """
    Checks for a number of given 3D labyrinths with start and end position for an escape route.
    If such an escape is possible, it prints the number of steps (= minutes) needed.
    Otherwise, it informs you that no exit is possible.

    :param input_filename: filename of a txt file with labyrinth descriptions
    """
    matrix = input_to_matrix(input_filename)
    for labyrinth_matrix in matrix:
        graph = to_graph(get_air_coordinates(labyrinth_matrix))
        start = 0
        end = len(graph)-1
        distance = shortest_path(graph, start, end)
        if distance == math.inf:
            print('Gefangen :-(')
        else:
            print(f'Entkommen in {distance} Minute(n)!')


if __name__ == '__main__':
    escape_labyrinths('input.txt')
