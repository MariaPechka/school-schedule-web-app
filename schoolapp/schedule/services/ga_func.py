from deap import base
from deap import creator
from deap import tools
import random
import matplotlib.pyplot as plt
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from apiapp import models
from .. import ga_seializers


# Получаем все объекты нужных моделей
subjects = models.Subject.objects.all()
classes = models.Class.objects.all().annotate(
    class_name = Concat(
        'eduparallel__year', 'letter',
        output_field=CharField()
    )
)
teachers = models.Teacher.objects.all().annotate(
    full_name = Concat('surname', Value(' '), 'first_name', Value(' '), 'last_name',
                       output_field=CharField()
    )
)
complexities = models.Complexity.objects.all()


# Создаем сущности для ГА
TEACHERS = list(teachers.values_list('full_name', 'subjects__title'))
CLASSES = list(classes.values_list('class_name', 'eduparallel__edu_complexities__subject__title', 'eduparallel__edu_complexities__complexity'))
TIME = {
    'Понедельник': (1, 2, 3, 4, 5, 6, 7, 8)
}


print(TEACHERS)
# print(CLASSES)









