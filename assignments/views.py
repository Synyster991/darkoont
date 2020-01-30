from django.shortcuts import render, redirect, get_object_or_404
from .models import AssignmentTeacherSide, studentAssignments


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


def detail(request, assignment_id):
    assignment = get_object_or_404(AssignmentTeacherSide, pk=assignment_id)

    return render(request, 'assignments/detail.html', {"assignment": assignment})


def teacherAssignments(request):
    assignments = AssignmentTeacherSide.objects

    return render(request, 'assignments/teacherAssignments.html', {"assignments": assignments})


def submitAssignmentStudent(request, assignment_id):
    tempAssignment = studentAssignments()
    realAssignment = assignment = get_object_or_404(AssignmentTeacherSide, pk=assignment_id)

    if request.method == 'POST':
        tempAssignment.assignment = realAssignment
        tempAssignment.points = 0
        tempAssignment.document = request.FILES['myfile']
        tempAssignment.studentUser = request.user
        tempAssignment.save()
    
    return redirect('home')