# Generated by Django 2.2.9 on 2020-01-28 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_auto_20200128_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentteacherside',
            name='teacherUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
