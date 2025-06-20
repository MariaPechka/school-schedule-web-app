from rest_framework import serializers
from django import forms

from apiapp import models


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = models.Classroom
        fields = ('name', 'type', 'capacity')
        labels = {
            'name': 'Название',
            'type': 'Тип',
            'capacity': 'Вместимость',
        }
        help_texts = {
            'capacity': 'Кол-во мест в кабинете'
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = models.Class
        fields = ('eduparallel', 'letter', 'student_amount', 'own_classroom')
        labels = {
            'eduparallel': 'Учебная параллель',
            'letter': 'Буква',
            'student_amount': 'Кол-во учеников',
            'own_classroom': 'Свой класс',
        }
        help_texts = {
            
        }


class TeacherSubjectsClass(forms.ModelForm):
    class Meta:
        model = models.Lesson
        fields = ('class_id', 'subject_id', 'teacher_id')
        labels = {
            'class_id': 'Класс',
            'subject_id': 'Предмет',
            'teacher_id': 'Учитель',
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ('surname', 'first_name', 'last_name', 'subjects', 'eduparallels')
        labels = {
            'surname': 'Фамилия',
            'first_name': 'Имя',
            'last_name': 'Отчество',
            'subjects': 'Предметы',
            'eduparallels': 'Учебные параллели',
        }
        help_texts = {
            'subjects': 'Которые ведет данный педагог',
            'eduparallels': 'У которых преподает данный педагог',
        }


class SchoolUserForm(forms.ModelForm):
    class Meta:
        model = models.SchoolUser
        fields = ('surname', 'first_name', 'last_name', 'email', 'role', 'password')
        labels = {
            'surname': 'Фамилия',
            'first_name': 'Имя',
            'last_name': 'Отчество',
            'email': 'Email',
            'role': 'Должность',
            'password': 'Пароль',
        }
        help_texts = {
        }



