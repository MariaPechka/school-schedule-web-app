from apiapp.services.insert_data import insert_levels, insert_eduparallels, insert_subjects, insert_complexity
from .parce_word import dict_edupar_subject_compl, sbj_list
from .parce_word import dict_level_edupar





insert_levels(dict_level_edupar)      
insert_eduparallels(dict_level_edupar)
insert_subjects(sbj_list)
insert_complexity(dict_edupar_subject_compl) 