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


class ScheduleGAModel:
    def __get_teacher_data(self):
        teachers = api_models.Teacher.objects.all().annotate(
            full_name = Concat('surname', Value(' '), 'first_name', Value(' '), 'last_name',
                            output_field=CharField()
            )
        )
        return teachers
    
    def __get_teacher_df(self):
        teachers = self.__get_teacher_data()
        teacher_sbj = list(teachers.values_list(
                                        'id',   
                                        'full_name', 
                                        'subjects__id', 
                                        'subjects__title'
                                        )
        )
        teachers_df = pd.DataFrame(teacher_sbj, 
                                    columns=[
                                        'teacher_id', 
                                        'full_name', 
                                        'subjects_id', 
                                        'subjects_title'
                                        ]
        )
        return teachers_df

    def __get_teacher_edge(self):
        teachers_df = self.__get_teacher_df()
        teach40_edge = [(f'{counter}.{i}', f'{counter}.{j}') 
                        for i in range(40) 
                        for j in range(i+1, 40) 
                        for counter in teachers_df['teacher_id'].unique()
                        ]
        return teach40_edge


    def __get_lesson_data(self):
        classes = api_models.Class.objects.all().annotate(
            class_name = Concat(
            'eduparallel__year', 'letter',
            output_field=CharField()
            )
        )   
        return classes
    
    def __get_lesson_df(self):
        classes = self.__get_lesson_data()
        lessons = list(classes.values_list(
                                        'class_name', 
                                        'eduparallel__edu_complexities__subject__id', 
                                        'eduparallel__edu_complexities__subject__title', 
                                        'eduparallel__edu_complexities__complexity', 
                                        'eduparallel__edu_complexities__hours_per_week'
                                        )
                        )
        lesson_df = pd.DataFrame(lessons,
                                columns=[
                                    'class_name',
                                    'subject_id',
                                    'subject_title',
                                    'complexity',
                                    'hours_per_week'
                                ]
        )
        return lesson_df

    def __get_lesson_edge(self):
        lessons_df = self.__get_lesson_df()
        lesson_edge = []
        for class_n in lessons_df['class_name'].unique():
            class_mas = []
            mask = lessons_df['class_name'] == str(class_n)
            for lesson in lessons_df[['class_name','subject_id', 'hours_per_week']][mask].to_numpy():
                for hour in range(lesson[2]):
                    m = f'{class_n}.{lesson[1]}.{hour}'
                    class_mas.append(m)
            for i in range(len(class_mas)):
                for j in range(i+1, len(class_mas)):
                    lesson_edge.append((class_mas[i], class_mas[j]))
        return lesson_edge


    def __init__(self):
        teach40_edge = self.__get_teacher_edge()
        lessons_edge = self.__get_lesson_edge()
        self.G = nx.Graph()
        self.G.add_edges_from(teach40_edge)
        self.G.add_edges_from(lessons_edge)
        
    def plotGraph(self):        
        options = {
            'node_color': 'pink', 
            'node_size': 100,
            'width': 1,
            'arrowstyle': '-|>',
            'font_size': 10,
        }
        nx.draw_networkx(self.G, pos=nx.spring_layout(self.G), with_labels = False, arrows=False, **options)
        plt.show()

