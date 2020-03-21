
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:assignment_id>', views.detail, name='detail'),
    path('teacherAssignments/', views.teacherAssignments, name='teacherAssignments'),
    path('<int:assignment_id>/', views.submitAssignmentStudent, name='submitAssignmentStudent'),
    path('showGrades/', views.showGrades, name='showGrades'),
    path('gradeStudent/', views.gradeStudent, name='gradeStudent'),
    path('seeMyGrades/', views.seeMyGrades, name='seeMyGrades'),
    path('seeSubmissions/', views.seeSubmissions, name='seeSubmissions'),
    path('seeSectionStudents/', views.seeSectionStudents, name='seeSectionStudents'),
    path('seeGradesPerSection/', views.seeGradesPerSection, name='seeGradesPerSection')
]
