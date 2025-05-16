from django.db import models

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

    def __str__(self):
        # return f'{str(self.year)} - {None}'
        return f'{str(self.year)} - {self.level.title}'
    

class Complexity(models.Model):
    eduparallel = models.ForeignKey(Eduparallel, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    complexity = models.IntegerField(blank=False)

    def __str__(self):
        # return f'{None} - {None} {self.subject.title.upper()} {self.complexity}'
        return f'{self.eduparallel.year} - {self.eduparallel.level} {self.subject.title.upper()} {self.complexity}'


