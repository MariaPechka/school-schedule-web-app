from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import itertools
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from .schedule_gcp_classes import ScheduleGSPGA as GraphClass

from apiapp import models
# import schedule.models as sch_models
# from .. import ga_seializers
# from .gcp_class import GraphColoringProblem
# from .elitism_func import eaSimpleWithElitism
# from .schedule_ga_model_class import ScheduleGAModel




def eaSimpleWithElitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
    halloffame is used to implement an elitism mechanism. The individuals contained in the
    halloffame are directly injected into the next generation and are not subject to the
    genetic operators of selection, crossover and mutation.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(halloffame.items)

        # Update the hall of fame with the generated individuals
        halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook


def run_ga():
    # Пробую ГА на функциях класса gcpz 
    POPULATION_SIZE = 300
    P_CROSSOVER = 0.8
    P_MUTATION = 0.1
    MAX_GENERATIONS = 400
    HALL_OF_FAME_SIZE = 5
    MAX_COLORS = 40

    HARD_CONSTRAINT_PENALTY = 100

    gcp = GraphClass(HARD_CONSTRAINT_PENALTY)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("Integers", random.randint, 0, MAX_COLORS - 1)
    toolbox.register("individualCreator", tools.initRepeat,
    creator.Individual, toolbox.Integers, len(gcp))
    toolbox.register("populationCreator", tools.initRepeat, list,
    toolbox.individualCreator)

    def getCost(individual):
        return gcp.getCost(individual), 
    toolbox.register("evaluate", getCost)

    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0,
    up=MAX_COLORS - 1, indpb=1.0/len(gcp))

    population = toolbox.populationCreator(n=POPULATION_SIZE)

    population, logbook = eaSimpleWithElitism(population,
    toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
    ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    solution = hof.items[0]
    print("Лучший индивидуум = ", )
    print("solution = ", solution)
    print("number of colors = ", gcp.getNumberOfColors(solution))
    print("Number of violations = ", gcp.getViolationsCount(solution))
    print("Number of gaps =   1 ->", gcp.no_first_3_lessons(solution)[0], "  2 ->", gcp.no_first_3_lessons(solution)[1], "  3 ->", gcp.no_first_3_lessons(solution)[2])
    print("Cost = ", gcp.getCost(solution))
# 
    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    plt.plot(minFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Поколение')
    plt.ylabel('Макс/средняя приспособленность')
    plt.title('Зависимость максимальной и средней приспособленности от поколения')

    plt.show()
    return gcp, solution



def schedule_from_nodes(graph: GraphClass, solution):
    subject_data = dict(models.Subject.objects.values_list('id', 'title'))
    nodes = graph.nodeList
    class_names = list(models.Class.objects.all().annotate(
        class_name = Concat('eduparallel__year', 'letter',
                             output_field=CharField())
        ).values_list('class_name', ))
    class_dict = {class_name[0]: {} for class_name in class_names}
    new_nodes_arr = []
    for node, time in zip(nodes, solution):
        split_node = node.split('.')
        sbj_title = subject_data[int(split_node[1])]
        new_node = f'{split_node[0]}-{sbj_title}-{split_node[2]}'
        class_dict[split_node[0]].update({time: new_node})
    schedule_arr = np.full((len(class_names), 40), '...').tolist()
    for i, class_name in enumerate(class_dict):
        for position in class_dict[class_name]:
            schedule_arr[i][position] = class_dict[class_name][position]
    np_order = np.array(schedule_arr).reshape(len(class_names), 5, 8)
    schedule_arr = [class_obj.T for class_obj in np_order]
    
    return schedule_arr


def test_ga_slasses(func=GraphClass.plotGraph, func1=GraphClass.plotGraphC):
# solution_udachnoe = [0, 34, 25, 11, 18, 24, 10, 9, 12, 1, 17, 30, 8, 7, 16, 33, 26, 20, 4, 31, 32, 2, 4, 18, 30, 17, 35, 25, 26, 34, 9, 10, 8, 16, 13, 33, 1, 24, 3, 39, 0, 5, 32, 2, 21, 25, 10, 33, 32, 36, 
# 20, 39, 8, 31, 1, 24, 35, 13, 34, 0, 17, 19, 9, 16, 29, 2, 18, 5, 11, 26, 31, 16, 8, 9, 2, 37, 17, 27, 24, 1, 28, 34, 22, 30, 33, 11, 18, 26, 10, 0, 3, 36, 7, 32, 25, 13, 1, 32, 35, 24, 9, 17, 16, 39, 26, 18, 10, 2, 25, 34, 8, 11, 33, 0, 20, 29, 19, 5, 2, 0, 24, 16, 26, 18, 23, 8, 10, 32, 34, 28, 1, 17, 9, 25, 34, 32, 22, 37, 29, 16, 25, 8, 18, 12, 10, 33, 1, 2, 17, 24, 19, 4, 36, 26, 9, 0, 18, 11, 1, 8, 19, 7, 39, 24, 37, 2, 25, 16, 32, 12, 34, 9, 26, 33, 17, 29, 10, 0]
    # solution = [24, 8, 29, 12, 10, 33, 18, 22, 32, 25, 6, 26, 17, 36, 34, 2, 0, 4, 16, 21, 1, 9, 1, 19, 17, 32, 21, 24, 0, 10, 9, 33, 8, 14, 16, 35, 2, 23, 18, 31, 25, 26, 7, 34, 36, 24, 18, 0, 25, 27, 16, 5, 3, 10, 31, 9, 11, 14, 20, 34, 21, 2, 35, 17, 32, 8, 33, 26, 1, 15, 24, 17, 2, 1, 34, 16, 22, 0, 12, 18, 20, 10, 9, 8, 3, 19, 32, 37, 25, 35, 14, 33, 13, 26, 31, 23, 33, 7, 8, 2, 13, 16, 32, 
    # 26, 0, 25, 24, 17, 1, 34, 15, 20, 18, 9, 10, 33, 36, 34, 19, 11, 8, 16, 1, 25, 9, 0, 17, 26, 32, 2, 18, 24, 10, 4, 2, 10, 28, 30, 25, 17, 0, 34, 8, 19, 1, 9, 38, 18, 16, 35, 32, 23, 7, 24, 33, 26, 12, 9, 37, 24, 16, 32, 15, 33, 17, 22, 26, 11, 8, 0, 10, 2, 1, 18, 19, 34, 13, 25]
    solution = [34, 18, 27, 20, 3, 11, 8, 9, 33, 25, 16, 32, 17, 12, 10, 0, 35, 1, 2, 26, 24, 19, 26, 2, 22, 3, 10, 9, 28, 16, 21, 27, 11, 8, 32, 33, 24, 1, 0, 25, 18, 34, 17, 12, 10, 11, 3, 13, 4, 1, 
17, 20, 33, 16, 25, 12, 27, 35, 2, 9, 32, 0, 26, 36, 34, 8, 19, 18, 28, 24, 18, 25, 1, 35, 19, 9, 24, 16, 17, 2, 0, 33, 32, 34, 20, 27, 26, 4, 11, 8, 10, 13, 12, 3, 36, 28, 33, 26, 34, 25, 17, 32, 16, 2, 8, 10, 3, 35, 0, 1, 18, 9, 36, 27, 24, 2, 0, 9, 3, 18, 34, 32, 27, 17, 8, 33, 35, 26, 25, 10, 1, 24, 16, 4, 27, 26, 33, 1, 9, 19, 11, 8, 28, 35, 17, 0, 34, 3, 18, 2, 25, 10, 32, 16, 36, 24, 21, 9, 26, 8, 33, 24, 22, 0, 17, 34, 2, 25, 1, 17, 20, 32, 27, 18, 19, 28, 16, 10]
    gcp = GraphClass(40)
    func_res = func(gcp)
    func_res1 = func1(gcp, solution)
    return gcp, solution, func_res, func_res1
# plot = gcp.plotGraphC(solution)
# plot.show()

# test_schedule = schedule_from_nodes(gcp, solution)



# Очень странное решение : 
# number of colors =  25
# Number of violations =  4
# Number of gaps =   1 -> -1   2 -> -3   3 -> 0
# Cost =  65
# solution =  [24, 27, 16, 33, 10, 11, 32, 
#              8, 9, 19, 12, 2, 0, 17, 3, 
#              25, 34, 26, 1, 20, 18, 4, 4,
#                3, 1, 5, 18, 17, 9, 19, 20,
#                  33, 32, 34, 10, 16, 21, 24,
#                    8, 25, 2, 0, 26, 35, 9, 24, 37, 
#                    38, 18, 16, 34, 36, 11, 35, 26, 17
#                    , 27, 33, 25, 19, 12, 4, 3, 0, 8, 1
#                    , 32, 13, 10, 2, 34, 1, 27, 17, 6,
#                      16, 33, 7, 3, 11, 4, 0, 32, 26, 24, 13
#                      , 8, 25, 9, 28, 18, 19, 10, 5, 2, 12
#                      , 25, 11, 9, 8, 24, 32, 10, 18, 17, 0, 
#                      33, 16, 34, 26, 3, 4, 35, 2, 1, 0,
#                        2, 16, 25, 8, 32, 35, 1, 34, 10, 20, 17,
#                          24, 9, 26, 19, 33, 36, 18, 36, 34, 16,
#                            24, 8, 28, 2, 20, 1, 18, 19, 26, 0, 9, 25,
#                              32, 10, 37, 17, 27, 33, 35, 18, 8, 35, 28,
#                                32, 33, 25, 10, 17, 27, 16, 19, 26,
#                                  2, 1, 36, 0, 20, 24, 11, 9, 34]
