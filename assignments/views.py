from django.shortcuts import render, redirect, get_object_or_404
from .models import AssignmentTeacherSide, studentAssignments, Sections
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import studentAssignments
from django.contrib import messages

def create(request):
    availableSection = []

    userName = request.user.get_username()
    user = User.objects.get(username=userName)
    availableSection = Sections.objects.filter(owner=user)

    try:
        if request.method == 'POST':
            if request.POST['title'] and request.POST['date'] and request.POST['instructions']:
                assignment = AssignmentTeacherSide()
                tempSection = Sections.objects.get(name=request.POST['sectionName'])

                assignment.title = request.POST['title']
                assignment.section = tempSection
                assignment.dueDate = request.POST['date']
                assignment.instructions = request.POST['instructions']
                assignment.maxPoint = request.POST['points']
                assignment.teacherUser = request.user
                assignment.teacherDocument = request.FILES['teacherfile']
                assignment.videoLink = request.POST['video']
                assignment.save()

                messages.info(request, 'Assignment Created!')
                return redirect('home')
            else:
                return render(request, 'assignments/create.html', {"error":"All fields are required!", "availableSection": availableSection})
        else:
            return render(request, 'assignments/create.html', {"availableSection": availableSection})
    except:
        messages.info(request, 'Assignment Not Created!')
        return render(request, 'assignments/create.html', {"availableSection": availableSection})


def detail(request, assignment_id):
    user = User.objects.get(username=request.user)
    assignment = get_object_or_404(AssignmentTeacherSide, pk=assignment_id)
    try:
        submittedAssignment = studentAssignments.objects.get(studentUser=request.user, assignment=assignment)
        allowSubmission = False
    except studentAssignments.DoesNotExist:
        allowSubmission = True

    return render(request, 'assignments/detail.html', {"assignment": assignment, "allowSubmission": allowSubmission})


def teacherAssignments(request):
    user = User.objects.get(username=request.user)
    tempSection = Sections.objects.get(owner=user)
    assignments = AssignmentTeacherSide.objects.filter(section=tempSection)

    return render(request, 'assignments/teacherAssignments.html', {"assignments": assignments})


def submitAssignmentStudent(request, assignment_id):
    tempAssignment = studentAssignments()
    realAssignment = get_object_or_404(AssignmentTeacherSide, pk=assignment_id)

    try:
        if request.method == 'POST':
            tempAssignment.assignment = realAssignment
            tempAssignment.points = -1
            tempAssignment.document = request.FILES['myfile']
            tempAssignment.studentUser = request.user
            tempAssignment.save()
            messages.info(request, 'Assignment Submitted!')
    except:
        messages.info(request, 'Assignment is not Submitted! Please Try again.')
        pass

    return redirect('home')


def showGrades(request):
    validAssignments = []
    user = ""

    try:
        if request.method == 'POST':
            user = User.objects.get(username=request.POST['studentID'])
            assignments = studentAssignments.objects

            for assignment in assignments.all():
                if assignment.studentUser == user:
                    validAssignments.append(assignment)
    except:
        pass

    return render(request, 'assignments/gradeStudent.html', {"validAssignments": validAssignments, "studentInfo": user})
    

def gradeStudent(request):
    # try:
    if request.method == 'POST':
        studentID = User.objects.get(username=request.POST['studentID'])
        assignmentID = AssignmentTeacherSide.objects.get(pk=request.POST['assignmentID'])
        tempGrade = request.POST['gradeID']
        assignment = studentAssignments.objects.get(studentUser=studentID, assignment=assignmentID)
        assignmentPK = assignment.pk
            
        gradeThisAssignment = get_object_or_404(studentAssignments, pk=assignmentPK)
        tempGrade = int(tempGrade)

        if tempGrade < 0:
            tempGrade = 0
        elif tempGrade > gradeThisAssignment.assignment.maxPoint:
            tempGrade = gradeThisAssignment.assignment.maxPoint
            
        gradeThisAssignment.points = tempGrade
        gradeThisAssignment.save()
        messages.info(request, 'Assignment Graded!')

        return redirect('home')
    # except:
    #     messages.info(request, 'Assignment is not ready to be graded!')
    #     return redirect('home')


def seeMyGrades(request):
    assignments = studentAssignments.objects.all()
    gradedAssignments = []

    for assignment in assignments:
        if assignment.studentUser == request.user: 
            gradedAssignments.append(assignment) 

    return render(request, 'assignments/seeMyGrades.html', {"gradedAssignments": gradedAssignments, "student":request.user})


def seeSubmissions(request):
    try:
        if request.method == 'POST':
            tempAssignment = AssignmentTeacherSide.objects.get(id=request.POST['assignmentID'])
            submissions = studentAssignments.objects.filter(assignment=tempAssignment)

        return render(request,'assignments/seeSubmissions.html', {"submissions": submissions, "tempAssignment":tempAssignment})
    except:
        return redirect('home')