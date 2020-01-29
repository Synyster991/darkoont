from django.shortcuts import render, redirect
from .models import AssignmentTeacherSide


def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['date'] and request.POST['instructions']:
            assignment = AssignmentTeacherSide()

            assignment.title = request.POST['title']
            assignment.dueDate = request.POST['date']
            assignment.instructions = request.POST['instructions']
            assignment.maxPoint = request.POST['points']
            assignment.teacherUser = request.user
            assignment.save()

            return render(request, 'accounts/home.html', {"isTeacher":True})
        else:
            return render(request, 'assignments/create.html', {"error":"All fields are required!"})
    else:
        return render(request, 'assignments/create.html')

    return render(request, 'assignments/create.html')