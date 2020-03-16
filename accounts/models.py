from django.db import models
from django.contrib.auth.models import User
from assignments.models import Sections

# Create your models here.
class StudentsTable(models.Model):
    studentFK = models.ForeignKey(User, on_delete=models.CASCADE)
    sectionFK = models.ForeignKey(Sections, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.studentFK, self.sectionFK)


class TeachersTable(models.Model):
    teacherFK = models.ForeignKey(User, on_delete=models.CASCADE)
    sectionFK = models.ForeignKey(Sections, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.sectionFK)