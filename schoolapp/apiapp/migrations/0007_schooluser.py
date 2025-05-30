# Generated by Django 5.1.7 on 2025-05-22 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0006_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Директор'), (2, 'Учитель'), (3, 'Завуч')])),
                ('password', models.CharField()),
            ],
        ),
    ]
