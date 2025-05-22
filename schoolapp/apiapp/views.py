from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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


def list_classroom(request):
    classrooms = models.Classroom.objects.all().order_by('name')
    return render(request, 'classroom/classroom_list.html', {'posts': classrooms})


def classroom_detail(request, pk):
    post = get_object_or_404(models.Classroom, pk=pk)
    return render(request, 'classroom/classroom_detail.html', {'post': post})


def add_classroom(request):
    if request.method == "POST":
        form = forms.ClassroomForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('classroom_detail', pk=post.pk)
    else:
        form = forms.ClassroomForm()
    return render(request, 'classroom/classroom_edit.html', {'form': form})


def edit_classroom(request, pk):
    classroom = get_object_or_404(models.Classroom, pk=pk)
    if request.method == "POST":
        form = forms.ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            post = form.save()
            return redirect('classroom_detail', pk=post.pk)
    else:
        form = forms.ClassroomForm(instance=classroom)
    return render(request, 'classroom/classroom_edit.html', {'form': form})



def add_class(request):
    form = forms.ClassForm()
    return render(request, 'class_edit.html', {'form': form})


def add_teacher(request):
    form = forms.TeacherForm()
    return render(request, 'teacher_edit.html', {'form': form})


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