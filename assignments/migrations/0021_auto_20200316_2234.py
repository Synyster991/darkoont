# Generated by Django 2.2.9 on 2020-03-17 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0020_auto_20200316_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentteacherside',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.Sections'),
        ),
    ]