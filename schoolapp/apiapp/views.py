from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
import requests

from apiapp.models import Level,  Eduparallel, Subject, Complexity
from apiapp.serializers import LevelSerializer, EduarallelSerializer
from apiapp.serializers import SubjectSerializer, ComplexitySerializer


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