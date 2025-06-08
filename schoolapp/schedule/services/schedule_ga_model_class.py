from itertools import combinations
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Value, CharField
from django.db.models.functions import Concat

import apiapp.models as api_models
from .gcp_class import GraphColoringProblem


class ScheduleGAModel:
    def __init__(self):
        self.GTeachNodes, self.GTeachEdge = self.__get_teacher_node_edge()
        self.GLessonNodes, self.GLessonEdge = self.__get_lesson_node_edge()
        self.G = nx.Graph()
        for teach in self.GTeachEdge:
            self.G.add_edges_from(teach) 
        for lesson in self.GLessonEdge:
            self.G.add_edges_from(lesson) 
    
        # super().__init__()


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

    def __get_teacher_node_edge(self):
        teachers_df = self.__get_teacher_df()
        teach40_nodes = []
        
        for counter in teachers_df['teacher_id'].unique():
            mask = teachers_df['teacher_id'] == counter
            subjects = teachers_df['subjects_id'][mask].to_list()
            teacher_nodes = []
            for i in range(40):
                print(subjects)
                teacher_nodes.append(f'{counter}.{subjects}.{i}')
            teach40_nodes.append(teacher_nodes)
        teach40_edge = [combinations(nodes, 2) for nodes in teach40_nodes]
        
        return teach40_nodes, teach40_edge

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
        nx.draw_networkx(self.G, pos=nx.spring_layout(self.G), with_labels = False, arrows=False, **options)
        plt.show()


# class ScheduleGAModel:
#     def __init__(self):
#         self.GTeachNodes, self.GTeachEdge = self.__get_teacher_node_edge()
#         self.GLessonNodes, self.GLessonEdge = self.__get_lesson_node_edge()
#         self.G = nx.Graph()
#         for teach in self.GTeachEdge:
#             self.G.add_edges_from(teach) 
#         for lesson in self.GLessonEdge:
#             self.G.add_edges_from(lesson) 
    
#         # super().__init__()


#     def __get_teacher_data(self):
#         teachers = api_models.Teacher.objects.all().annotate(
#             full_name = Concat('surname', Value(' '), 'first_name', Value(' '), 'last_name',
#                             output_field=CharField()
#             )
#         )
#         return teachers
    
#     def __get_teacher_df(self):
#         teachers = self.__get_teacher_data()
#         teacher_sbj = list(teachers.values_list(
#                                         'id',   
#                                         'full_name', 
#                                         'subjects__id', 
#                                         'subjects__title'
#                                         )
#         )
#         teachers_df = pd.DataFrame(teacher_sbj, 
#                                     columns=[
#                                         'teacher_id', 
#                                         'full_name', 
#                                         'subjects_id', 
#                                         'subjects_title'
#                                         ]
#         )
#         return teachers_df

#     def __get_teacher_node_edge(self):
#         teachers_df = self.__get_teacher_df()
#         teach40_nodes = []
        
#         for counter in teachers_df['teacher_id'].unique():
#             mask = teachers_df['teacher_id'] == counter
#             subjects = teachers_df['subjects_id'][mask].to_list()
#             teacher_nodes = []
#             for i in range(40):
#                 print(subjects)
#                 teacher_nodes.append(f'{counter}.{subjects}.{i}')
#             teach40_nodes.append(teacher_nodes)
#         teach40_edge = [combinations(nodes, 2) for nodes in teach40_nodes]
        
#         return teach40_nodes, teach40_edge

#     def __get_lesson_data(self):
#         classes = api_models.Class.objects.all().annotate(
#             class_name = Concat(
#             'eduparallel__year', 'letter',
#             output_field=CharField()
#             )
#         )   
#         return classes
    
#     def __get_lesson_df(self):
#         classes = self.__get_lesson_data()
#         lessons = list(classes.values_list(
#                                         'class_name', 
#                                         'eduparallel__edu_complexities__subject__id', 
#                                         'eduparallel__edu_complexities__subject__title', 
#                                         'eduparallel__edu_complexities__complexity', 
#                                         'eduparallel__edu_complexities__hours_per_week'
#                                         )
#                         )
#         lesson_df = pd.DataFrame(lessons,
#                                 columns=[
#                                     'class_name',
#                                     'subject_id',
#                                     'subject_title',
#                                     'complexity',
#                                     'hours_per_week'
#                                 ]
#         )
#         return lesson_df

#     def __get_lesson_node_edge(self):
#         lessons_df = self.__get_lesson_df()
#         lesson_nodes = []
#         for class_n in lessons_df['class_name'].unique():
#             class_mas = []
#             mask = lessons_df['class_name'] == str(class_n)
#             for lesson in lessons_df[['class_name','subject_id', 'hours_per_week']][mask].to_numpy():
#                 for hour in range(lesson[2]):
#                     m = f'{class_n}.{lesson[1]}.{hour}'
#                     class_mas.append(m)
#             lesson_nodes.append(class_mas)

#         lesson_edge = [combinations(mas, 2) for mas in lesson_nodes]

#         return lesson_nodes, lesson_edge
    
        
#     def plotGraph(self):        
#         options = {
#             'node_color': 'pink', 
#             'node_size': 100,
#             'width': 1,
#             'font_size': 10,
#         }
#         nx.draw_networkx(self.G, pos=nx.spring_layout(self.G), with_labels = False, arrows=False, **options)
#         plt.show()


# G = ScheduleGAModel()
# mas_nodes = G.GTeachNodes
# mas_edges_test = [list(combinations(mas, 2)) for mas in mas_nodes]
# mas_edge = G.GTeachEdge

# print(mas_edges_test)
# print(mas_edge)

# G.plotGraph()
# test = GraphColoringProblem(G.G, 40)

# print(test.adjMatrix)


# print(test.nodeList)




# nodes = ['A', 'B', 'C', 'D']

# G = nx.Graph()
# G.add_nodes_from(nodes)
# G.add_edges_from(combinations(nodes, 2))

# print(G.edges)
# print(G.nodes)

# options = {
#     'node_color': 'pink', 
#     'node_size': 100,
#     'width': 1,
#     'font_size': 10,
# }
# nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels = False, arrows=False, **options)
# plt.show()