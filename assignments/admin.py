from django.contrib import admin

from .models import AssignmentTeacherSide, studentAssignments

admin.site.register(AssignmentTeacherSide)
admin.site.register(studentAssignments)