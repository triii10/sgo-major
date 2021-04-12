from src.Logger import log
from random import random 
from os import chdir
from os.path import abspath, join
from math import sqrt
from math import log as math_log

def calculate_euclidean_distance(a, b):
    return sqrt(((a[0] - b[0])**2) + ((a[1] - b[1])**2))*1000
    
def calculate_distance_from_base_station(a, base_station):
    return sqrt(((a[0] - base_station[0]) ** 2) + ((a[1] - base_station[1]) ** 2) + (base_station[2]**2))*1000

def normalizer(val):
    return math_log(val)

def generate_random_row(col):
    '''
    genarate a random row of 0 and 1 of size 'row'
    '''
    init_row = []
    for _ in range(col):
        init_row.append(random())

    log("init_row : ", init_row)
    return init_row

def generate_population(nodes):
    '''
    Generate a random sparse matrix of size row * col
    '''

    init_population = []
    for _ in range(nodes):
        init_population.append(generate_random_row(nodes))

    log("init_population : ", init_population)
    
    return init_population

def get_adjacency_matrix():
    path = abspath("data")

    nodes = 0
    adjacency_matrix = []
    with open(join(path, "graph.txt")) as file:
        nodes = int(file.readline()) - 1
        for _ in range(nodes):
            line = file.readline()
            adjacency_matrix.append([*map(int, line.split(','))])

    log("Adjacency Matrix : ", adjacency_matrix)
    return nodes, adjacency_matrix

def get_time_matrix(nodes):
    path = abspath("data")
    time_matrix = []

    def convert_type(num):
        try:
            num = int(num)
            return num
        except:
            return -1

    with open(join(path, "time.txt")) as file:
        for _ in range(nodes):
            line = file.readline()
            time_matrix.append([*map(convert_type, line.split(','))])

    log("Time Matrix : ", time_matrix)
    return time_matrix

def get_cost_matrix(nodes):
    path = abspath("data")
    cost_matrix = []

    def convert_type(num):
        try:
            num = int(num)
            return num
        except:
            return -1

    with open(join(path, "cost.txt")) as file:
        for _ in range(nodes):
            line = file.readline()
            cost_matrix.append([*map(convert_type, line.split(','))])

    log("Cost Matrix : ", cost_matrix)
    return cost_matrix


def get_min_index(vector):
    min_val = min(vector)
    for i, val in enumerate(vector):
        if(min_val == val):
            return i

    return 0

def get_second_min_index(vector):
    min_index = get_min_index(vector)
    second_min_index = 0
    for i, val in enumerate(vector):
        if val > vector[min_index] and val < vector[second_min_index]:
            second_min_index = i

    return second_min_index

def get_max_index(vector):
    max_val = max(vector)
    for i, val in enumerate(vector):
        if(max_val == val):
            return i

    return 0