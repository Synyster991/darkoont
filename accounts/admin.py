from django.contrib import admin

from .models import StudentsTable, TeachersTable

admin.site.register(StudentsTable)
admin.site.register(TeachersTable)