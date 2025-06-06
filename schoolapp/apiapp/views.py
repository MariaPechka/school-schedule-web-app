from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet
import requests

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User


from apiapp.models import Level,  Eduparallel, Subject, Complexity
from apiapp import models
from apiapp.serializers import LevelSerializer, EduarallelSerializer
from apiapp.serializers import SubjectSerializer, ComplexitySerializer
from apiapp import serializers
from apiapp import forms


class LevelViewSet(ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class EduparallelViewSet(ModelViewSet):
    queryset = Eduparallel.objects.all()
    serializer_class = EduarallelSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ComplexityViewSet(ModelViewSet):
    queryset = Complexity.objects.all()
    serializer_class = ComplexitySerializer


# class TeacherViewSet(ModelViewSet):
#     queryset = models.Teacher.objects.all()#.prefetch_related('subjects')
#     serializer_class = serializers.TeacherSerializer

#     @action(methods=['get'], detail=False)
#     def lists(self, request):
#         return render(request, 'teacher/list_teacher.html', {'teachers': self.queryset})
    

#     @action(methods=['get'], detail=False)
#     def teacher_detail(self, request, **kwargs):
#         pk = kwargs.keys
#         # teacher = get_object_or_404(models.Teacher, pk=pk)
#         return render(request, 'teacher/detail_teacher.html', {'k':pk})




# Classroom methods
def list_classroom(request):
    classrooms = models.Classroom.objects.all().order_by('name')
    return render(request, 'classroom/classroom_list.html', {'posts': classrooms})


def detail_classroom(request, pk):
    post = get_object_or_404(models.Classroom, pk=pk)
    return render(request, 'classroom/classroom_detail.html', {'post': post})


def add_classroom(request):
    if request.method == "POST":
        form = forms.ClassroomForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('detail_classroom', pk=post.pk)
    else:
        form = forms.ClassroomForm()
    return render(request, 'classroom/classroom_edit.html', {'form': form})


def edit_classroom(request, pk):
    classroom = get_object_or_404(models.Classroom, pk=pk)
    if request.method == "POST":
        form = forms.ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('list_classroom')
    else:
        form = forms.ClassroomForm(instance=classroom)
    return render(request, 'classroom/classroom_edit.html', {'form': form})



# Class Methods
def class_list(request):
    classes = models.Class.objects.all().order_by('eduparallel', 'letter')
    return render(request, 'class/list_class.html', {'classes': classes})

def class_detail(request, pk):
    class_obj = get_object_or_404(models.Class, pk=pk)
    return render(request, 'class/detail_class.html', {'class': class_obj})

def class_add(request):
    if request.method == "POST":
        form = forms.ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save()
            class_obj.save()
            return redirect('class_list')
    else:
        form = forms.ClassForm()
    return render(request, 'class/edit_class.html', {'form': form})

def class_edit(request, pk):
    class_get_obj = get_object_or_404(models.Class, pk=pk)
    if request.method == "POST":
        form = forms.ClassForm(request.POST, instance=class_get_obj)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = forms.ClassForm(instance=class_get_obj)
    return render(request, 'class/edit_class.html', {'form': form})



def teacher_list(request):
    teachers = models.Teacher.objects.all().prefetch_related('subjects').order_by(
        'surname', 
        'first_name', 
        'last_name'
    )
    return render(request, 'teacher/list_teacher.html', {'teachers': teachers})

def teacher_detail(request, pk):
    teacher = get_object_or_404(models.Teacher, pk=pk)
    return render(request, 'teacher/detail_teacher.html', {'teacher': teacher})

def teacher_add(request):
    if request.method == "POST":
        form = forms.TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = forms.TeacherForm()
    return render(request, 'teacher/edit_teacher.html', {'form': form})

def teacher_edit(request, pk):
    teacher = get_object_or_404(models.Teacher, pk=pk)
    if request.method == "POST":
        form = forms.TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = forms.TeacherForm(instance=teacher)
    return render(request, 'teacher/edit_teacher.html', {'form': form})





def add_schooluser(request):
    form = forms.SchoolUserForm()
    return render(request, 'schooluser_edit.html', {'form': form})







# Create your views here.
# def show_lessons(request):
#     all_complexity = Complexity.objects.all()
#     all_eduparallel = Eduparallel.objects.all()
#     return render (request=request, template_name='lessons.html', context={'comp_list': all_complexity, 'eduparal_list': all_eduparallel})



# def get_complexity(request):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
#     }
#     url = 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fsh-pavlovskaya-r66.gosweb.gosuslugi.ru%2Fnetcat_files%2F22%2F3341%2FShkala_trudnosti_uchebnyh_predmetov.doc&wdOrigin=BROWSELINK'
#     response = requests.get(url, headers=headers)
#     print(type(response))
#     return HttpResponse('Good!')