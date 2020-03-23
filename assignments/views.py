from django.shortcuts import render, redirect, get_object_or_404
from .models import AssignmentTeacherSide, studentAssignments, Sections
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from accounts.models import StudentsTable
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, login_required
from django.utils.translation import gettext as _


@login_required(login_url="/accounts/signup")
@user_passes_test(lambda u: u.groups.filter(name='Teacher').exists())
def create(request):
    # Creating assignment from the teacher side
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
                assignment.maxPoint = 100
                assignment.teacherUser = request.user
                assignment.teacherDocument = request.FILES['teacherfile']
                assignment.videoLink = request.POST['video']
                assignment.save()

                messages.info(request, _('Assignment Created!'))
                return redirect('home')
            else:
                return render(request, 'assignments/create.html', {"error":_("All fields are required!"), "availableSection": availableSection})
        else:
            return render(request, 'assignments/create.html', {"availableSection": availableSection})
    except:
        messages.info(request, _('Assignment Not Created!'))
        return render(request, 'assignments/create.html', {"availableSection": availableSection})


@login_required(login_url="/accounts/signup")
def detail(request, assignment_id):
    # Students can see details about the assignments and limiting submission to one time
    user = User.objects.get(username=request.user)
    assignment = get_object_or_404(AssignmentTeacherSide, pk=assignment_id)
    
    try:
        submittedAssignment = studentAssignments.objects.get(studentUser=request.user, assignment=assignment)
        allowSubmission = False
    except studentAssignments.DoesNotExist:
        allowSubmission = True

    return render(request, 'assignments/detail.html', {"assignment": assignment, "allowSubmission": allowSubmission})


@login_required(login_url="/accounts/signup")
@user_passes_test(lambda u: u.groups.filter(name='Teacher').exists())
def teacherAssignments(request):
    # Teacher can see their own created assignments

    checkedAssignments = []
    user = User.objects.get(username=request.user)
    tempSection = Sections.objects.filter(owner=user)
    assignments = AssignmentTeacherSide.objects.filter(teacherUser=user)

    for assign in assignments:
        if assign.section in tempSection:
            checkedAssignments.append(assign)

    return render(request, 'assignments/teacherAssignments.html', {"checkedAssignments":checkedAssignments})


@login_required(login_url="/accounts/signup")
def submitAssignmentStudent(request, assignment_id):
    # Allowing students to submit their assignment
    tempAssignment = studentAssignments()
    realAssignment = get_object_or_404(AssignmentTeacherSide, pk=assignment_id)

    try:
        if request.method == 'POST':
            tempAssignment.assignment = realAssignment
            tempAssignment.points = -1
            tempAssignment.document = request.FILES['myfile']
            tempAssignment.studentUser = request.user
            tempAssignment.save()
            messages.info(request, _('Assignment Submitted!'))
    except:
        messages.info(request, _('All fields are required'))
        messages.info(request, _('Assignment is not Submitted! Please Try again.'))

    return redirect('home')


@login_required(login_url="/accounts/signup")
def showGrades(request):
    # Teacher can see assignments, grades, submission and download assignments.
    validAssignments = []
    user = ""

    try:
        if request.method == 'POST':
            totalScore = 0
            averageScore = 0.0
            counterForGradedAssignments = 0
            user = User.objects.get(username=request.POST['studentIDforGrade'])
            sectionName = request.POST['sectionIDforGrade']
            assignments = studentAssignments.objects

            for assignment in assignments.all():
                if assignment.studentUser == user and assignment.assignment.section.name == sectionName:
                    validAssignments.append(assignment)
                    if assignment.points != -1:
                        counterForGradedAssignments += 1
                        totalScore += assignment.points

            try:
                averageScore = "{0:.2f}".format(totalScore / counterForGradedAssignments)
            except ZeroDivisionError:
                averageScore = "{0:.2f}".format(totalScore / 1)

        if validAssignments == []:
            messages.info(request, _('Student not found!'))
            return redirect('home')
        else:
            return render(request, 'assignments/gradeStudent.html', {"validAssignments": validAssignments, "studentInfo": user, "averageScore": averageScore, "sectionName": sectionName})
    except:
        messages.info(request,  _('Student not found!'))
        return redirect('home')

    


@login_required(login_url="/accounts/signup")    
@user_passes_test(lambda u: u.groups.filter(name='Teacher').exists())
def gradeStudent(request):
    # Grade student functionallity
    try:
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
            messages.info(request, _('Assignment Graded!'))

            return redirect('home')
    except:
        # If the student didn't submit, teache can still give him a grade
        try:
            if request.method == 'POST':
                studentID = User.objects.get(username=request.POST['studentID'])
                assignmentID = AssignmentTeacherSide.objects.get(pk=request.POST['assignmentID'])
                studentAssignments.objects.get(studentUser=studentID, assignment=assignmentID)
        except studentAssignments.DoesNotExist:
            studentID = User.objects.get(username=request.POST['studentID'])
            assignmentID = AssignmentTeacherSide.objects.get(pk=request.POST['assignmentID'])

            notSubmitted = studentAssignments()
            notSubmitted.assignment = assignmentID
            notSubmitted.points = request.POST['gradeID']
            notSubmitted.document = '/static/student.png'
            notSubmitted.studentUser = studentID
            notSubmitted.save()

        messages.info(request, _('Assignment Graded!'))
        return redirect('home')


@login_required(login_url="/accounts/signup")    
def seeMyGrades(request):
    # Students can see their own grades
    assignments = studentAssignments.objects.all()
    gradedAssignments = []

    for assignment in assignments:
        if assignment.studentUser == request.user: 
            gradedAssignments.append(assignment) 

    return render(request, 'assignments/seeMyGrades.html', {"gradedAssignments": gradedAssignments, "student":request.user})


@login_required(login_url="/accounts/signup")    
@user_passes_test(lambda u: u.groups.filter(name='Teacher').exists())
def seeSubmissions(request):
    # Teachers can see submission for unique assignments
    try:
        if request.method == 'POST':
            tempAssignment = AssignmentTeacherSide.objects.get(id=request.POST['assignmentID'])
            submissions = studentAssignments.objects.filter(assignment=tempAssignment)

        return render(request,'assignments/seeSubmissions.html', {"submissions": submissions, "tempAssignment":tempAssignment})
    except:
        messages.info(request, _('Submissions not found'))
        return redirect('home')


def seeSectionStudents(request):
    # See Section's students
    try:
        if request.method == 'POST':
            # Prevent from unnecesery error
            if request.POST['sectionID'] == "empty":
                messages.info(request, _('Section not found!'))
                return redirect('home')

            sectionID = request.POST['sectionID']
            checkedStudents = []
            allStudents = StudentsTable.objects.filter()

            for student in allStudents:
                if student.sectionFK.name == sectionID:
                    checkedStudents.append(student) 

        return render(request, 'assignments/seeSectionStudents.html', {"checkedStudents": checkedStudents, "sectionID": sectionID})
    except:
        messages.info(request, _('Section not found!'))
        return redirect('home')


def seeGradesPerSection(request):
    # Allows students to see grades for each section and calculate their average score
    try:
        if request.method == 'POST':
            # Prevent from unnecesery error
            if request.POST['sectionID'] == "empty":
                messages.info(request, _('Section not found!'))
                return redirect('home')

            checkedSubmissions = []
            totalScore = 0
            averageScore = 0.0
            counterForGradedAssignments = 0
            sectionID = request.POST['sectionID']
            submittedAssignments = studentAssignments.objects.filter(studentUser=request.user)

            for assignment in submittedAssignments:
                if assignment.assignment.section.name == sectionID:
                    checkedSubmissions.append(assignment)
                    if assignment.points != -1:
                        counterForGradedAssignments += 1
                        totalScore += assignment.points

            try:
                averageScore = "{0:.2f}".format(totalScore / counterForGradedAssignments)
            except ZeroDivisionError:
                averageScore = "{0:.2f}".format(totalScore / 1)

            return render(request, 'assignments/seeGradesPerSection.html', {"sectionID": sectionID, "checkedSubmissions": checkedSubmissions, "averageScore": averageScore})
    except:
        messages.info(request, _('Section not found!'))
        return redirect('home')