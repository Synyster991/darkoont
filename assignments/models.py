from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AssignmentTeacherSide(models.Model):
    title = models.CharField(max_length=50)
    instructions = models.TextField()
    maxPoint = models.IntegerField()
    dueDate = models.DateTimeField()
    teacherUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title