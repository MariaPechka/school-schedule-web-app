from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apiapp.models import Level, Eduparallel, Subject
from apiapp.services.insert_data import insert_levels, insert_eduparallels, insert_subjects
from apiapp.serializers import LevelSerializer, EduarallelSerializer, SubjectSerializer

from apiapp.services.parce_word import dict_edupar_subject_compl

class InsertDataApiTestCase(APITestCase):
    def setUp(self):
        self.level_year_dict = {
            'Level 1': [0,1,2,3],
            'Level 2': [4,5,6],
            'Level 3': [7,8,9,10,11],
        }
        self.sbj_list = ['Maths', 'English', 'PE', 'Computer Science']
        self.user = User.objects.create(username='auth_user1')

    def test_insert_levels(self):
        self.assertEqual(0, Level.objects.all().count())
        insert_levels(self.level_year_dict)
        self.assertEqual(3, Level.objects.all().count())
        url = reverse('level-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_response = LevelSerializer(Level.objects.all(), many=True)
        self.assertCountEqual(serializer_response.data, response.data)

    def test_insert_edupararalells(self):
        insert_levels(self.level_year_dict)
        
        self.assertEqual(0, Eduparallel.objects.all().count())
        insert_eduparallels(self.level_year_dict)
        self.assertEqual(12, Eduparallel.objects.all().count())
        url = reverse('eduparallel-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_response = EduarallelSerializer(Eduparallel.objects.all(), many=True)
        self.assertCountEqual(serializer_response.data, response.data)

    def test_insert_subjects(self):
        self.assertEqual(0, Subject.objects.all().count())
        insert_subjects(self.sbj_list)
        self.assertEqual(4, Subject.objects.all().count())
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_response = SubjectSerializer(Subject.objects.all(), many=True)
        self.assertCountEqual(serializer_response.data, response.data)

        