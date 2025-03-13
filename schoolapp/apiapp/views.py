from django.shortcuts import render
from django.http import HttpResponse
import requests
from apiapp.models import Complexity, Eduparallel

# Create your views here.
def show_lessons(request):
    all_complexity = Complexity.objects.all()
    all_eduparallel = Eduparallel.objects.all()
    return render (request=request, template_name='lessons.html', context={'comp_list': all_complexity, 'eduparal_list': all_eduparallel})