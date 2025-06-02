from django.db import models

import apiapp.models as api_models


class Lesson(models.Model):
    complexity = models.ForeignKey(api_models.Complexity, on_delete=models.SET_NULL, null=True, related_name='compl_for_class')
    class_m = models.ForeignKey(api_models.Class, on_delete=models.SET_NULL, null=True, related_name='class_for_compl')


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(api_models.Teacher, on_delete=models.SET_NULL, null=True, related_name='teacher_for_sbj')
    subject = models.ForeignKey(api_models.Subject, on_delete=models.SET_NULL, null=True, related_name='sbj_for_teacher')
