from deap import base
from deap import creator
from deap import tools
import random
import itertools
from itertools import combinations
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from apiapp import models
# from .ga_func import eaSimpleWithElitism


class GraphColoringProblem:
    """This class encapsulates the Graph Coloring problem
    """

    def __init__(self, graph, hardConstraintPenalty):
        """
        :param graph: a NetworkX graph to be colored
        :param hardConstraintPenalty: penalty for hard constraint (coloring violation)
        """

        # initialize instance variables:
        self.graph = graph
        self.hardConstraintPenalty = hardConstraintPenalty

        # a list of the nodes in the graph:
        self.nodeList = list(self.graph.nodes)

        # adjacency matrix of the nodes -
        # matrix[i,j] equals '1' if nodes i and j are connected, or '0' otherwise:
        self.adjMatrix = nx.adjacency_matrix(graph).todense()
        # super().__init__()

    def __len__(self):
        """
        :return: the number of nodes in the graph
        """
        return nx.number_of_nodes(self.graph)

    def getCost(self, colorArrangement):
        """
        Calculates the cost of the suggested color arrangement
        :param colorArrangement: a list of integers representing the suggested color arrangement for the nodes,
        one color per node in the graph
        :return: Calculated cost of the arrangement.
        """

        return self.hardConstraintPenalty * self.getViolationsCount(colorArrangement) + self.getNumberOfColors(colorArrangement)

    def getViolationsCount(self, colorArrangement):
        """
        Calculates the number of violations in the given color arrangement. Each pair of interconnected nodes
        with the same color counts as one violation.
        :param colorArrangement: a list of integers representing the suggested color arrangement for the nodes,
        one color per node in the graph
        :return: the calculated value
        """

        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color arrangement should be equal to ", self.__len__())

        violations = 0

        # iterate over every pair of nodes and find if they are adjacent AND share the same color:
        for i in range(len(colorArrangement)):
            for j in range(i + 1, len(colorArrangement)):

                if self.adjMatrix[i, j]:    # these are adjacent nodes
                    if colorArrangement[i] == colorArrangement[j]:
                        violations += 1

        return violations

    def getNumberOfColors(self, colorArrangement):
        """
        returns the number of different colors in the suggested color arrangement
        :param colorArrangement: a list of integers representing the suggested color arrangement fpo the nodes,
        one color per node in the graph
        :return: number of different colors
        """
        return len(set(colorArrangement))

    def plotGraphC(self, colorArrangement):
        """
        Plots the graph with the nodes colored according to the given color arrangement
        :param colorArrangement: a list of integers representing the suggested color arrangement fpo the nodes,
        one color per node in the graph
        """

        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color list should be equal to ", self.__len__())

        # create a list of the unique colors in the arrangement:
        colorList = list(set(colorArrangement))

        # create the actual colors for the integers in the color list:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(colorList)))

        # iterate over the nodes, and give each one of them its corresponding color:
        colorMap = []
        for i in range(self.__len__()):
            color = colors[colorList.index(colorArrangement[i])]
            colorMap.append(color)

        # nx.draw_kamada_kawai
        # plot the nodes with their labels and matching colors:
        nx.draw_networkx(self.graph, pos=nx.spring_layout(self.graph), node_color=colorMap, node_size=100,
            width=1,
            font_size=10, with_labels=True)
        #nx.draw_circular(self.graph, node_color=color_map, with_labels=True)

        plt.show()


class ScheduleGAModel:
    def __init__(self):
        # self.GTeachNodes, self.GTeachEdge = self.__get_teacher_node_edge()
        self.GLessonNodes, self.GLessonEdge = self.__get_lesson_node_edge()
        self.classesAmount = len(self.GLessonNodes)
        self.G = nx.Graph()
        # for teach in self.GTeachEdge:
            # self.G.add_edges_from(teach) 
        for lesson in self.GLessonEdge:
            self.G.add_edges_from(lesson) 
    
        # super().__init__()


    def __get_teacher_data(self):
        teachers = models.Teacher.objects.all().annotate(
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

    def __get_teacher_node_edge(self):
        teachers_df = self.__get_teacher_df()
        teach40_nodes = []
        
        for counter in teachers_df['teacher_id'].unique():
            mask = teachers_df['teacher_id'] == counter
            subjects = teachers_df['subjects_id'][mask].to_list()
            teacher_nodes = []
            for i in range(40):
                # print(subjects)
                teacher_nodes.append(f'{counter}.{subjects}.{i}')
            teach40_nodes.append(teacher_nodes)
        teach40_edge = [combinations(nodes, 2) for nodes in teach40_nodes]
        
        return teach40_nodes, teach40_edge

    def __get_lesson_data(self):
        classes = models.Class.objects.all().annotate(
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

    def __get_lesson_node_edge(self):
        lessons_df = self.__get_lesson_df()
        lesson_nodes = []
        for class_n in lessons_df['class_name'].unique():
            class_mas = []
            mask = lessons_df['class_name'] == str(class_n)
            for lesson in lessons_df[['class_name','subject_id', 'hours_per_week']][mask].to_numpy():
                for hour in range(lesson[2]):
                    m = f'{class_n}.{lesson[1]}.{hour}'
                    class_mas.append(m)
            lesson_nodes.append(class_mas)

        lesson_edge = [combinations(mas, 2) for mas in lesson_nodes]

        return lesson_nodes, lesson_edge
    
        
    def plotGraph(self):        
        options = {
            'node_color': 'pink', 
            'node_size': 100,
            'width': 1,
            'font_size': 10,
        }
        nx.draw_networkx(self.G, pos=nx.spring_layout(self.G), with_labels = True, arrows=False, **options)
        plt.show()




class ScheduleGSPGA(ScheduleGAModel, GraphColoringProblem):
    def __init__(self, hardConstraintPenalty): 
        ScheduleGAModel.__init__(self)
        GraphColoringProblem.__init__(self, self.G, hardConstraintPenalty)
        # self.teacher_nodes_range = sum([len(teacher) for teacher in self.GTeachNodes])
        # self.lessons_nodes_range = sum([len(lesson) for lesson in self.GLessonNodes]) + self.teacher_nodes_range


    def getCost(self, colorArrangement):
        """
        Calculates the cost of the suggested color arrangement
        :param colorArrangement: a list of integers representing the suggested color arrangement for the nodes,
        one color per node in the graph
        :return: Calculated cost of the arrangement.
        """

        return self.hardConstraintPenalty * self.getViolationsCount(colorArrangement) +\
            40*sum(self.no_first_3_lessons(colorArrangement)) +\
            35*self.gaps_per_day(colorArrangement) +\
            20*self.max_lessons(colorArrangement) +\
            self.getNumberOfColors(colorArrangement)

    
    def no_first_3_lessons(self, colorArrangement):
        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
        count_1 = self.classesAmount*5 - sum([colorArrangement.count(first) for first in range(0,40,8)]) 
        count_2 = self.classesAmount*5 - sum([colorArrangement.count(second) for second in range(1,40,8)])
        count_3 = self.classesAmount*5 - sum([colorArrangement.count(third) for third in range(2,40,8)])
        count_1 = count_1 if count_1 > 0 else 0
        count_2 = count_2 if count_2 > 0 else 0
        count_3 = count_3 if count_3 > 0 else 0

        return count_1, count_2, count_3

    def gaps_per_day(self, colorArrangement):
        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
        class_lessons_lens = [len(class_obj) for class_obj in self.GLessonNodes]
        # class_names = [class_obj[0].split('.')[0] for class_obj in self.GLessonNodes]
        
        count_gaps = 0      
        count = 0
        # for i, name in zip(class_lessons_lens, class_names):
        #     print(name)
        for i in class_lessons_lens:
            class_lessons_range = colorArrangement[count: count+i]
            
            # for day_name, day in zip(range(1,6), range(0,40,8)):
            for day in range(0,40,8):
                mask = [lesson in class_lessons_range for lesson in range(day, day+8)]
                # print(day_name, '-->', mask)
                work_hours = 0
                for lesson in range(7,0,-1):
                    if mask[lesson]:
                        work_hours = lesson
                        break
                count_per_day = mask[0:work_hours].count(False)
                # print(day_name, '-->', count_per_day)
                count_gaps += count_per_day
                    
            count += i
            # print()
        return count_gaps
    
    def more_then_1(self, colorArrangement):
        pass
    def max_lessons(self, colorArrangement):
        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
        class_lessons_lens = [len(class_obj) for class_obj in self.GLessonNodes]
        # class_names = [class_obj[0].split('.')[0] for class_obj in self.GLessonNodes]
        
        too_much = 0
        count = 0
        # for i, name in zip(class_lessons_lens, class_names):
        for i in class_lessons_lens:
            # print(name)
            class_lessons = colorArrangement[count: count+i]

            # for day_name, day in zip(range(1,6), range(0,40,8)):
            for day in range(0,40,8):
                day_sum = 0
                for lesson in range(day, day+8):
                    day_sum +=  lesson in class_lessons
                if day_sum > 5:
                    too_much += day_sum - 5
                    # too_much += 1
                # print('day:', day_name, '-->', day_sum, 'lessons --> too_much', too_much)

            count += i
        return too_much
    # def gaps_per_day(self, colorArrangement):
    #     if len(colorArrangement) != self.__len__():
    #         raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
    #     class_lessons_lens = [len(class_obj) for class_obj in self.GLessonNodes]
    #     class_names = [class_obj[0].split('.')[0] for class_obj in self.GLessonNodes]
        
    #     count_gaps = 0      
    #     count = 0
    #     for i, name in zip(class_lessons_lens, class_names):
    #         print(name)
    #     # for i in class_lessons_lens:
    #         class_lessons_range = colorArrangement[count: count+i]
            
    #         for day_name, day in zip(range(1,6), range(0,40,8)):
    #         # for day in range(0,40,8):
    #             for lesson in range(day, day+8):
    #                 if lesson == day+7 and \
    #                     lesson in class_lessons_range and \
    #                     lesson-2 not in class_lessons_range and \
    #                     lesson-1 not in class_lessons_range:
    #                     print('day:', day_name, lesson-1, '<--', lesson)
    #                     count_gaps += 1
    #                 elif lesson != day+7 and \
    #                     not lesson in class_lessons_range and \
    #                     lesson+1 in class_lessons_range :
    #                     # (lesson+1 in class_lessons_range or \
    #                     # lesson+2 in class_lessons_range) :
    #                     # lesson-1 in class_lessons_range and \
    #                     print('day:', day_name, lesson-1, '<--', lesson, '-->', lesson+1)
    #                     count_gaps += 1
    #                 elif lesson != day+7 and \
    #                     lesson not in class_lessons_range and\
    #                     lesson+1 not in class_lessons_range and\
    #                     lesson-1 not in class_lessons_range :
    #                     count_gaps += 1
    #                     print('day:', day_name, lesson-1, '<--', lesson, '-->', lesson+1)
                        
                    
    #         count += i
    #         # print()
    #     return count_gaps
        
    # def gaps_per_day(self, colorArrangement):
    #     if len(colorArrangement) != self.__len__():
    #         raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
    #     count_gaps = 0      
    #     for day in range(0, 40, 8):
    #         for i in range(day, day+8):
    #             amount_i = colorArrangement.count(i)
    #             amount_next_i = colorArrangement.count(i+1)
    #             diff = amount_i - amount_next_i
    #             if diff < 0:
    #                 # print(i, '&', i+1, 'diff =', diff)
    #                 count_gaps += abs(diff)
    #     return count_gaps
    


                
            # print('count:', count, '   count+i:', count+i)

    # def lesson_teacher_related(self, colorArrangement):
    #     if len(colorArrangement) != self.__len__():
    #         raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
    #     violations = 0
    #     for color in set(colorArrangement):
    #         teachers_color = []
    #         lessons_color = []
    #         for i, item in enumerate(colorArrangement):
    #             if item == color and i < self.teacher_nodes_range:
    #                 teacher_id = self.nodeList[i]
    #                 teachers_color.append(teacher_id)
    #             if item == color and i < self.lessons_nodes_range:
    #                 lesson_id = self.nodeList[i]
    #                 lessons_color.append(lesson_id)
    #         if len(teachers_color) != len(lessons_color):
    #             violations += 1
    #         print(f'color: {color}   teachers: {teachers_color}   lessons: {lessons_color}')
    #         return violations
        






