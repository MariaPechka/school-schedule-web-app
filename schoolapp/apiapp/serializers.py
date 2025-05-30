from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apiapp.models import Level, Eduparallel, Subject, Complexity
from apiapp import models


class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class EduarallelSerializer(ModelSerializer):
    class Meta:
        model = Eduparallel
        fields = '__all__'


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ComplexitySerializer(ModelSerializer):
    class Meta:
        model = Complexity
        fields = '__all__'


class TeacherSerializer(ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    eduparallels = EduarallelSerializer(many=True, read_only=True)
    class Meta:
        model = models.Teacher
        fields = '__all__'






