from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=60, blank=False, unique=True)

    def __str__(self):
        return self.title
    

class Level(models.Model):
    title = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.title


class Eduparallel(models.Model):
    year = models.IntegerField(blank=False)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True)
    subjects = models.ManyToManyField(Subject, through='Complexity', related_name='rel_parallels')

    def __str__(self):
        return f'{str(self.year)}'
        # return f'{str(self.year)} - {self.level.title}'
    

class Complexity(models.Model):
    eduparallel = models.ForeignKey(Eduparallel, on_delete=models.SET_NULL, null=True, related_name='edu_complexities')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='sbj_complexity')
    complexity = models.SmallIntegerField(blank=False)
    hours_per_week = models.SmallIntegerField(null=True, default=None)

    def __str__(self):
        # return f'{None} - {None} {self.subject.title.upper()} {self.complexity}'
        return f'{self.eduparallel.year} - {self.eduparallel.level} {self.subject.title.upper()} {self.complexity} ---- {self.hours_per_week}h'


class Classroom(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    ROOM_TYPE_CHOICES = (
        ('classroom', 'Кабинет'),
        ('gym', 'Спортзал'),
        ('hall', 'Актовый зал'),
        ('tech', 'Кабинет технологии'),
        ('physics', 'Кабинет физики'),
        ('chemistry', 'Кабинет химии'),
        ('informatics', 'Кабинет информатики'),
        ('art', 'Кабинет ИЗО'),
    )
    type = models.CharField(choices=ROOM_TYPE_CHOICES, null=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.type} - {self.capacity}'


class Class(models.Model):
    eduparallel = models.ForeignKey(Eduparallel, on_delete=models.PROTECT)
    LETTER_CHOICES = (
        ('А', 'А'),
        ('Б', 'Б'),
        ('В', 'В'),
        ('Г', 'Г'),
        ('Д', 'Д'),
    )
    letter = models.CharField(choices=LETTER_CHOICES, blank=False)
    own_classroom = models.OneToOneField(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    student_amount = models.PositiveIntegerField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['eduparallel', 'letter'], name='unique_class'),
        ]

    def __str__(self):
        return f'{self.eduparallel.year}{self.letter}'
    

class Teacher(models.Model):
    surname = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True)
    subjects = models.ManyToManyField(Subject)
    eduparallels = models.ManyToManyField(Eduparallel)

    def __str__(self):
        return f'{self.surname} {self.first_name} {self.last_name}'


class SchoolUser(models.Model):
    surname = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, unique=True)
    ROLE_CHOICE = (
        (1, 'Директор'),
        (2, 'Учитель'),
        (3, 'Завуч'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=False)
    password = models.CharField(blank=False)