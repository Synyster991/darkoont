# Generated by Django 2.2.8 on 2020-03-23 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0024_homework'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentteacherside',
            name='startDate',
        ),
        migrations.DeleteModel(
            name='HomeWork',
        ),
    ]
