from .parce_word import dict_edupar_subject_compl, sbj_list
from .parce_word import dict_level_edupar
from apiapp.models import Level, Subject, Complexity, Eduparallel


def insert_levels(dict_level_edupar:dict):
    for level in dict_level_edupar:
        Level.objects.create(title=level)


def insert_eduparallels(dict_level_edupar:dict):
    for level in dict_level_edupar:
        level_obj = Level.objects.get(title=level)
        for par in dict_level_edupar[level]:
            Eduparallel.objects.create(year=par,
                                    level=level_obj)


def insert_subjects(sbj_list:list):
    for sbj in sbj_list:
        Subject.objects.create(title=sbj)


def insert_complexity(dict_edupar_subject_compl:dict):
    for edu in dict_edupar_subject_compl:
        edu_obj = Eduparallel.objects.get(year=edu)
        for sbj in dict_edupar_subject_compl[edu]:
            sbj_obj = Subject.objects.get(title=sbj)
            compl = dict_edupar_subject_compl[edu][sbj]
            Complexity.objects.create(eduparallel=edu_obj,
                                      subject=sbj_obj,
                                      complexity=compl)



                 