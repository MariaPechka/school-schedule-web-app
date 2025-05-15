from spire.doc import *
from spire.doc.common import *


doc = Document()

# doc.LoadFromFile("..\\dop-data\\Shkala_trudnosti_uchebnyh_predmetov.doc")
doc.LoadFromFile("apiapp\\dop-data\\Shkala_trudnosti_uchebnyh_predmetov.doc")

# Словарь с уровнями образования и классами
dict_level_edupar = {
    'Начальное общее': [1,2,3,4],
    'Основное общее' : [5,6,7,8,9],
    'Среднее общее'  : [10,11],
}

# Словарь с классами
dict_edupar_subject_compl = {
    1 : {},
    2 : {},
    3 : {},
    4 : {},
    5 : {},
    6 : {},
    7 : {},
    8 : {},
    9 : {},
    10: {},
    11: {},
}

sbj_list = []

for i in range(doc.Sections.Count):
    section = doc.Sections.get_Item(i)
    tables = section.Tables

    # Цикл по таблицам сложности предметов в документе для каждого уровня общего образования (0-начальное, 1-основное, 2-среднее)
    for j in range(tables.Count):
        table = tables.get_Item(j)

        for row in range(table.Rows.Count):
            sbj_compl = []   # Создание списка со сложность предмета для классов
            for col in range(table.Rows.get_Item(row).Cells.Count):
                cell = table.Rows.get_Item(row).Cells.get_Item(col)
                par_text = cell.Paragraphs.get_Item(0).Text    # Извлечение данных из ячейки таблицы
                
                # # Избавление от вложенности (Математика)
                # if '(' in par_text and 'Общ' not in par_text:
                #         par_text = par_text[par_text.index('(')+1 : par_text.index(')')].capitalize()

                sbj_compl.append(par_text) # Добавление значения ячейки в список             
            
            # Проверка, что в списке всего один предмет
            if not (sbj_compl[1].isdigit() or sbj_compl[1] == '-'):
                sbj_compl.pop(0)  # Убираем пропуск или лишний предмет 

            # Если в списке нет предмета или список состоит только из слов, данные не добавляются
            if len(sbj_compl[0])<2 or not (sbj_compl[-1].isdigit() or sbj_compl[-1] == '-'):
                continue

            # Добавление данных в словарь в соответствующие классы
            # if j==0:
            #     for eduparallel in range(1,5):
            #         dict_edupar_subject_compl[eduparallel][sbj_compl[0]] = sbj_compl[1]       
            # elif j==1:
            #     for ind, eduparallel in enumerate(range(5,10)):
            #         dict_edupar_subject_compl[eduparallel][sbj_compl[0]] = sbj_compl[ind+1]
            # elif j==2:
            #     sbj_split = sbj_compl[0].split(',')
            #     for sbj in sbj_split:
            #         if 'МХК' in sbj:
            #             sbj = 'Мировая художественная культура'
            #         for eduparallel in range(10,12):
            #             dict_edupar_subject_compl[eduparallel][sbj.strip()] = sbj_compl[1]  

            sbj_split = sbj_compl[0].split(',')
            # print(sbj_split)
            for sbj in sbj_split:
                sbj = sbj.strip()
                # Избавление от вложенности везде, кроме 'Обществознание (включая экономику и право)'
                if '(' in sbj and 'Общ' not in sbj:
                        sbj = sbj[sbj.index('(')+1 : sbj.index(')')].capitalize()

                if 'Мхк' in sbj:
                    sbj = 'Мировая художественная культура'

                sbj_list.append(sbj)

                for ind, eduparallel in enumerate(dict_level_edupar[list(dict_level_edupar.keys())[j]]):
                    dict_edupar_subject_compl[eduparallel][sbj] = sbj_compl[1] if len(sbj_compl) == 2 else sbj_compl[ind+1]
                

sbj_list = list(set(sbj_list))

# Вывод результата
def show_result(dict_edupar_subject_compl):
    for edupar in dict_edupar_subject_compl.keys():
        print(edupar, 'CLASS')
        for sbj in dict_edupar_subject_compl[edupar].keys():
            print(sbj, dict_edupar_subject_compl[edupar][sbj])
        print('\n')