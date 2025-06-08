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

from .gcp_class import GraphColoringProblem
from .elitism_func import eaSimpleWithElitism
from .schedule_ga_model_class import ScheduleGAModel


class ScheduleGSPGA(ScheduleGAModel, GraphColoringProblem):
    def __init__(self, hardConstraintPenalty): 
        ScheduleGAModel.__init__(self)
        GraphColoringProblem.__init__(self, self.G, hardConstraintPenalty)
        self.teacher_nodes_range = sum([len(teacher) for teacher in self.GTeachNodes])
        self.lessons_nodes_range = sum([len(lesson) for lesson in self.GLessonNodes]) + self.teacher_nodes_range
        if self.lessons_nodes_range != self.__len__():
            raise ValueError("size of color arrangement should be equal to ", self.__len__())
        

    def lesson_teacher_related(self, colorArrangement):
        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color arrangement should be equal to ", self.__len__())
        
        violations = 0
        for color in set(colorArrangement):
            teachers_color = []
            lessons_color = []
            for i, item in enumerate(colorArrangement):
                if item == color and i < self.teacher_nodes_range:
                    teacher_id = self.nodeList[i]
                    teachers_color.append(teacher_id)
                if item == color and i < self.lessons_nodes_range:
                    lesson_id = self.nodeList[i]
                    lessons_color.append(lesson_id)
            if len(teachers_color) != len(lessons_color):
                violations += 1
            print(f'color: {color}   teachers: {teachers_color}   lessons: {lessons_color}')
            return violations
        

    def get_teacher_subject(self, teachers_color):
        df = self.__get_teacher_df()
        teachers_subjects_color = []



test = ScheduleGSPGA(40)

print(test.GTeachNodes)
solution = np.random.randint(40, size=len(test))
# test.lesson_teacher_related(solution)

# plot = test.plotGraphC(solution)
# plot.show()
# test.plotGraph()





