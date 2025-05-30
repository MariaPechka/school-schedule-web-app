from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apiapp import models


# class LevelSerializer(ModelSerializer):
#     class Meta:
#         model = models.Level
#         fields = 'title'


class EduarallelSerializer(ModelSerializer):
    class Meta:
        model = models.Eduparallel
        fields = ('id', 'year')


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'title')


class ClassSerializer(ModelSerializer):
    # eduparallel = EduarallelSerializer(many=True, read_only=True)
    class Meta:
        model = models.Class
        fields = ('id', 'eduparallel', 'letter')


class ComplexitySerializer(ModelSerializer):
    # eduparallel = EduarallelSerializer(many=True, read_only=True)
    # subject = SubjectSerializer(many=True, read_only=True)
    # hours ???
    class Meta:
        model = models.Complexity
        fields = ('id', 'eduparallel', 'subject', 'complexity')



class TeacherSerializer(ModelSerializer):
    # subjects = SubjectSerializer(many=True, read_only=True)
    # # eduparallels = EduarallelSerializer(many=True, read_only=True)
    # full_name = serializers.CharField(read_only=True)

    class Meta:
        model = models.Teacher
        fields = ('id', 'subjects', 'full_name')

    # @staticmethod
    # def get_full_name(obj):
    #     obj.full_name = f'{obj.surname} {obj.first_name} {obj.last_name}'
    #     return obj.full_name

    # def to_representation(self, instance):
    #     # Получаем значения полей
    #     surname = instance.surname
    #     first_name = instance.first_name
    #     last_name = instance.last_name

    #     # Конкатенируем значения
    #     full_name = f"{surname} {first_name} {last_name}"

    #     # Возвращаем представление с конкатенированным полем
    #     representation = super().to_representation(instance)
    #     representation['full_name'] = full_name
    #     return representation
