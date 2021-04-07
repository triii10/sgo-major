from src.Logger import log
from math import ceil 
from random import random, choice
from copy import deepcopy


def fitness(population, src, dest, cost_matrix, time_matrix, phops, phops_modulus):
    '''
    Calculate the fitness value for each row of the matrix
    Returns the row having the maximum fitness
    '''

    init_fit = []

    def calculate_fitness(hop_destination, src, dest):

        alpha = random()
        log("Calculating fitness...")
        fit = 0
        log("src = ", src)
        log("dest = ", dest)
        while src != dest:
            log(src, "->")
            fit += (alpha)*time_matrix[src][hop_destination[src]] + (1-alpha)*cost_matrix[src][hop_destination[src]]
            src = hop_destination[src]
        log(dest)
        return fit

    for particles in population:
        hops, hop_destination = calculate_next_hops(particles, phops, phops_modulus)
        # print(hop_destination)
        init_fit.append(calculate_fitness(hop_destination, deepcopy(src), deepcopy(dest)))
        
    log("init_fit : ", init_fit)
    min_fitness = min(init_fit)
    for i, val in enumerate(init_fit):
        if val == min_fitness:
            return init_fit, population[i]


def calculate_next_phops(matrix):
    phops, phops_modulus = [], []
    for row in matrix:
        airport = []
        for i, val in enumerate(row):
            if val > 0:
                airport.append(i)
        phops.append(airport)
        phops_modulus.append(len(airport))

    # phops.pop()
    # phops_modulus.pop()
    log("phops : ", phops)
    log("|phops| : ", phops_modulus)
    return phops, phops_modulus

def calculate_next_hops(particles, phops, phops_modulus):
    hops = [*map(ceil, [x * y for x, y in zip(particles, phops_modulus)])]
    hops = [*map(min, zip(hops, phops_modulus))]
    
    log("hops : ", hops)

    hop_destination = []
    for node, next_node in zip(phops, hops):
        log("node : ", node)
        if(len(node) > 0):
            # if next_node > 0:
                hop_destination.append(node[next_node-1])
            # else:
            #     hop_destination.append(node[0])
        
    log("hop_destination : ", hop_destination)
    return hops, hop_destination

def improve_phase(adjacency_matrix, init_population, g_best_pop, init_fitness, src, dest, cost_matrix, time_matrix, phop, phops_modulus):
    '''
    Perform the improving phase and return the new matrix
    '''

    def calculate_X_new(x_old, g_best_pop_val):
        '''
        function to calculate the new X value
        '''
        c_val = 0.2
        r_val = random()

        return (c_val*x_old) + (r_val*(g_best_pop_val - x_old))

    final_fitness = []
    final_population = []
    # iterate each row in the population matrix
    for (i, row) in enumerate(init_population):
        
        new_row = []

        log("Calculating new X for row ", i)
        # iterate over each column value in the row, to caLculate the new row value
        for val, g_best_pop_val in zip(row, g_best_pop):
            # log("row_val, g_best_pop_val : ", val, g_best_pop_val)
            new_row.append(abs(calculate_X_new(val, g_best_pop_val)))

        new_fit, new_pop = fitness([new_row], deepcopy(src), deepcopy(dest), cost_matrix, time_matrix, phop, phops_modulus)
        if(new_fit[0] < init_fitness[i]):
           final_fitness.append(new_fit[0])
           final_population.append(new_pop)
        else:
            final_fitness.append(init_fitness[i])
            final_population.append(row)
        
    return final_population, final_fitness

def acquiring_phase(nodes, new_population, new_fitness, g_best_pop, src, dest, cost_matrix, time_matrix, phops, phops_modulus):

    for i in range(nodes):
        X_r_index = choice([x for x in range(nodes) if x != i])
        if new_fitness[X_r_index] > new_fitness[i]:
            def calculate_X_new(x_old, x_r, g_best_pop_val):    
                r1_val = random()
                r2_val = random()

                return (x_old) + r1_val*(x_old - x_r) + (r2_val*(g_best_pop_val - x_old))

            x_new = []
            for x_old, x_r, g_best_pop_val in zip(new_population[i], new_population[X_r_index], g_best_pop):
                x_new.append(abs(calculate_X_new(x_old, x_r, g_best_pop_val)))
            
            x_new_fit, _ = fitness([x_new], src, dest, cost_matrix, time_matrix, phops, phops_modulus)

            if(x_new_fit[0] < new_fitness[i]):
                new_fitness[i] = x_new_fit[0]
                new_population[i] = x_new
        else:
            def calculate_X_new(x_old, x_r, g_best_pop_val):    
                r1_val = random()
                r2_val = random()

                return (x_old) + r1_val*(x_r - x_old) + (r2_val*(g_best_pop_val - x_old))

            x_new = []
            for x_old, x_r, g_best_pop_val in zip(new_population[i], new_population[X_r_index], g_best_pop):
                x_new.append(abs(calculate_X_new(x_old, x_r, g_best_pop_val)))
            
            x_new_fit, _ = fitness([x_new], src, dest, cost_matrix, time_matrix, phops, phops_modulus)

            if(x_new_fit[0] < new_fitness[i]):
                new_fitness[i] = x_new_fit[0]
                new_population[i] = x_new

    return new_population, new_fitness