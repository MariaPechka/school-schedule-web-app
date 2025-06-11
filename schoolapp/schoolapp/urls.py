"""
URL configuration for schoolapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from apiapp.views import LevelViewSet, EduparallelViewSet
from apiapp.views import SubjectViewSet, ComplexityViewSet
from apiapp import views


router = SimpleRouter()
router.register(r'level', LevelViewSet)
router.register(r'eduparallel', EduparallelViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'complexity', ComplexityViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('classroom/', views.classroom_list, name='classroom_list'),
    path('classroom/new/', views.classroom_add, name='classroom_add'),
    path('classroom/<int:pk>/', views.classroom_detail, name='classroom_detail'),
    path('classroom/<int:pk>/edit/', views.classroom_edit, name='classroom_edit'),
    path('classroom/<int:pk>/delete', views.classroom_delete, name='classroom_delete'),

    path('class/', views.class_list, name='class_list'),
    path('class/new/', views.class_add, name='class_add'),
    path('class/<int:pk>/', views.class_detail, name='class_detail'),
    path('class/<int:pk>/edit', views.class_edit, name='class_edit'),
    path('class/<int:pk>/delete', views.class_delete, name='class_delete'),

    path('teacher/', views.teacher_list, name='teacher_list'),
    path('teacher/new/', views.teacher_add, name='teacher_add'),
    path('teacher/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teacher/<int:pk>/edit', views.teacher_edit, name='teacher_edit'),
    path('teacher/<int:pk>/delete', views.teacher_delete, name='teacher_delete'),

    path('schedule/prepare', views.schedule_prepare, name='schedule_prepare'),
    path('schedule/loading', views.start_ga, name='start_ga'),
    path('schedule/solution', views.show_ga_solution, name='show_ga_solution'),

    # path('post/teacher/', views.add_teacher, name='add_teacher'),

    # path('post/school-user/', views.add_schooluser, name='add_schooluser'),
]
urlpatterns += router.urls