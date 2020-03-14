from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AssignmentTeacherSide(models.Model):
    title = models.CharField(max_length=50)
    section = models.CharField(max_length=25)
    instructions = models.TextField()
    maxPoint = models.IntegerField()
    dueDate = models.DateTimeField()
    teacherDocument = models.FileField(upload_to='documents/', default="")
    videoLink = models.CharField(max_length=80, default="")
    teacherUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class studentAssignments(models.Model):
    assignment = models.ForeignKey(AssignmentTeacherSide, on_delete=models.CASCADE)
    points = models.IntegerField()
    document = models.FileField(upload_to='documents/')
    studentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # Title - Last Name First Name (points/maxPoints)
        return "{} - {} {} ({}/{})".format(self.assignment.title, self.studentUser.last_name, self.studentUser.first_name, self.points, self.assignment.maxPoint)

