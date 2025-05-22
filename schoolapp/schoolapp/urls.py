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
# router.register(r'add_classroom', add_classroom)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/classroom/', views.add_classroom, name='add_classroom'),
    path('post/class/', views.add_class, name='add_class'),
    path('post/teacher/', views.add_teacher, name='add_teacher'),
    path('post/school-user/', views.add_schooluser, name='add_schooluser'),
    # path('lessons/', show_lessons),
    # path('', get_complexity)
]
urlpatterns += router.urls