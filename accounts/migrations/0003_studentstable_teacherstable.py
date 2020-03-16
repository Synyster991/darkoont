# Generated by Django 2.2.9 on 2020-03-16 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assignments', '0016_sections'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20200128_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeachersTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.Sections')),
                ('teacherFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.Sections')),
                ('studentFK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
