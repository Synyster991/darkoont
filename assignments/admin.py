from django.contrib import admin

from .models import AssignmentTeacherSide, studentAssignments, Sections

admin.site.register(AssignmentTeacherSide)
admin.site.register(studentAssignments)
admin.site.register(Sections)