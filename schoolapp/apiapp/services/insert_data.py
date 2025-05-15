from .parce_word import dict_edupar_subject_compl, sbj_list
from .parce_word import dict_level_edupar as dle
from apiapp.models import Level, Subject, Complexity, Eduparallel


def insert_levels(dict_level_edupar:dict):
    for level in dict_level_edupar.keys():
        Level.objects.create(title=level)


def insert_eduparallels(dict_level_edupar:dict):
    for level in dict_level_edupar.keys():
        # print(dict_level_edupar[level])
        level_obj = Level.objects.get(title=level)
        for par in dict_level_edupar[level]:
            Eduparallel.objects.create(year=par,
                                    level=level_obj)


def insert_subjects(sbj_list:list):
    for sbj in sbj_list:
        Subject.objects.create(title=sbj)
