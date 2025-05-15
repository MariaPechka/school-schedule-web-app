from django.test import TestCase

from apiapp.serializers import LevelSerializer, EduarallelSerializer, SubjectSerializer
from apiapp.models import Level, Eduparallel, Subject


class LevelSerializerTestCase(TestCase):
    def test_ok(self):
        l1 = Level.objects.create(title='Level 1')
        l2 = Level.objects.create(title='Level 2')

        levels = Level.objects.all()
        serializer_data = LevelSerializer(levels, many=True).data
        expected_data = [
            {
            'id': l1.id,
            'title':'Level 1',
            },
            {
            'id': l2.id,
            'title':'Level 2',
            },
        ]
        self.assertEqual(expected_data, serializer_data)


class EduparallelSerializerTestCase(TestCase):
    def test_ok(self):
        l1 = Level.objects.create(title='Level 1')
        l2 = Level.objects.create(title='Level 2')
        edu1 = Eduparallel.objects.create(year=1, level=l1)
        edu2 = Eduparallel.objects.create(year=2, level=l1)
        edu3 = Eduparallel.objects.create(year=3, level=l2)

        edus = Eduparallel.objects.all()
        serializer_data = EduarallelSerializer(edus, many=True).data
        expected_data = [
            {
            'id': edu1.id,
            'year': 1,
            'level':l1.id,
            },
            {
            'id': edu2.id,
            'year': 2,
            'level':l1.id,
            },
            {
            'id': edu3.id,
            'year': 3,
            'level':l2.id,
            },
        ]
        self.assertEqual(expected_data, serializer_data)


class SubjectSerializerTestCase(TestCase):
    def test_ok(self):
        s1 = Subject.objects.create(title='Maths')
        s2 = Subject.objects.create(title='PE')

        sbjs = Subject.objects.all()
        serializer_data = SubjectSerializer(sbjs, many=True).data
        expected_data = [
            {
            'id': s1.id,
            'title':'Maths',
            },
            {
            'id': s2.id,
            'title':'PE',
            },
        ]
        self.assertEqual(expected_data, serializer_data)








