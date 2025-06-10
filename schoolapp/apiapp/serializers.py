from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apiapp.models import Level, Eduparallel, Subject, Complexity, Class
from apiapp import models


class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class EduparallelSerializer(ModelSerializer):
    class Meta:
        model = Eduparallel
        fields = 'subjects'


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = 'title'


class ComplexitySerializer(ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class ClassSerializer(ModelSerializer):
    subjects = EduparallelSerializer(many=True, read_only=True)
    class Meta:
        model = Class
        fields = ('id', 'eduparallel', 'letter', 'student_amount', 'subjects')


class TeacherSerializer(ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    eduparallels = EduparallelSerializer(many=True, read_only=True)
    class Meta:
        model = models.Teacher
        fields = '__all__'






