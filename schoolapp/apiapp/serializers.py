from rest_framework.serializers import ModelSerializer

from apiapp.models import Level, Eduparallel, Subject, Complexity


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




