from deap import base
from deap import creator
from deap import tools
import random
import itertools
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from django.db.models import Value, CharField
from django.db.models.functions import Concat

import apiapp.models as api_models
import schedule.models as sch_models
from .. import ga_seializers
from .gcp_class import GraphColoringProblem
from .elitism_func import eaSimpleWithElitism
from .schedule_ga_model_class import ScheduleGAModel

# Получаем все объекты нужных моделей
# subjects = api_models.Subject.objects.all()

# def __get_teacher_data():
#     teachers = api_models.Teacher.objects.all().annotate(
#         full_name = Concat('surname', Value(' '), 'first_name', Value(' '), 'last_name',
#                         output_field=CharField()
#         )
#     )
#     teacher_sbj = list(teachers.values_list(
#                                     'id',   
#                                     'full_name', 
#                                     'subjects__id', 
#                                     'subjects__title'
#                                     )
#     )
#     teachers_sbj_df = pd.DataFrame(teacher_sbj, 
#                                 columns=[
#                                     'teacher_id', 
#                                     'full_name', 
#                                     'subjects_id', 
#                                     'subjects_title'
#                                     ]
#     )
#     teach40_edge = [(f'{counter}.{i}', f'{counter}.{j}') 
#                     for i in range(40) 
#                     for j in range(i+1, 40) 
#                     for counter in teachers_sbj_df['teacher_id'].unique()
#                     ]
#     return teach40_edge


# def __get_lesson_data():
#     classes = api_models.Class.objects.all().annotate(
#     class_name = Concat(
#         'eduparallel__year', 'letter',
#         output_field=CharField()
#         )
#     )   
#     lessons = list(classes.values_list(
#                                     'class_name', 
#                                     'eduparallel__edu_complexities__subject__id', 
#                                     'eduparallel__edu_complexities__subject__title', 
#                                     'eduparallel__edu_complexities__complexity', 
#                                     'eduparallel__edu_complexities__hours_per_week'
#                                     )
#                     )
#     lessons_df = pd.DataFrame(lessons,
#                             columns=[
#                                 'class_name',
#                                 'subject_id',
#                                 'subject_title',
#                                 'complexity',
#                                 'hours_per_week'
#                             ]
#     )

#     lessons_edge = []
#     for class_n in lessons_df['class_name'].unique():
#         class_mas = []
#         mask = lessons_df['class_name'] == str(class_n)
#         for lesson in lessons_df[['class_name','subject_id', 'hours_per_week']][mask].to_numpy():
#             for hour in range(lesson[2]):
#                 m = f'{class_n}.{lesson[1]}.{hour}'
#                 class_mas.append(m)
#         for i in range(len(class_mas)):
#             for j in range(i+1, len(class_mas)):
#                 lessons_edge.append((class_mas[i], class_mas[j]))
#     return lessons_edge


# time = np.arange(1, 41).reshape(5,8)
# day_time = {
#     'Понедельник':time[0],
#     'Вторник'    :time[1],
#     'Среда'      :time[2],
#     'Четверг'    :time[3],
#     'Пятница'    :time[4],
# }

# # def create_individual(teachers_sbj_df, lessons_df):
# # У каждого учителя 40 уроков в неделю.
# # Составление ребер графа из пар времен учитея (40х40)
# # teach40_edge = [(f'{counter}.{i}', f'{counter}.{j}') 
# #                 for i in range(40) 
# #                 for j in range(i+1, 40) 
# #                 for counter in teachers_sbj_df['teacher_id'].unique()
# #                 ]




# options = {
#     'node_color': 'pink', 
#     'node_size': 100,
#     'width': 1,
#     'arrowstyle': '-|>',
#     # 'arrowsize': 18,
#     'font_size': 10,
# }

# # Создаем граф
# G = nx.Graph()
# G.add_edges_from(teach40_edge)
# G.add_edges_from(lessons_edge)
# nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels = False, arrows=False, **options)
# plt.show()







# Раскраска тест (успешно! :) Умничка!!!)
G = ScheduleGAModel()
gcp = GraphColoringProblem(G, 40)
# solution = np.random.randint(40, size=len(gcp))


# plot = gcp.plotGraph(solution)
# plot.show()


# Пробую ГА на функциях класса gcpz 
POPULATION_SIZE = 350
P_CROSSOVER = 0.9
P_MUTATION = 0.4
MAX_GENERATIONS = 300
HALL_OF_FAME_SIZE = 5
MAX_COLORS = 40

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
print("Cost = ", gcp.getCost(solution))

minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
plt.plot(minFitnessValues, color='red')
plt.plot(meanFitnessValues, color='green')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.show()