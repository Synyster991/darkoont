# Generated by Django 2.2.9 on 2020-03-17 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0019_auto_20200316_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentteacherside',
            name='section',
            field=models.CharField(max_length=25),
        ),
    ]
