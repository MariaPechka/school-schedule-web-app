from rest_framework.serializers import ModelSerializer

from apiapp.models import Level, Eduparallel, Subject


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




