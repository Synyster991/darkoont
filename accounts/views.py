from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group
from assignments.models import AssignmentTeacherSide, studentAssignments, Sections
from accounts.models import TeachersTable, StudentsTable
from datetime import datetime

def home(request):
    try:
        # Sync sections between teacher and students
        userName = request.user.get_username()
        user = User.objects.get(username=userName)
        tempSections = Sections.objects.filter(owner=user)
        studentSections = StudentsTable.objects.filter(studentFK=user)
        tempSectionsList = []
        validStudents = []
        studentAvailableAssignments = []
        teacherAssignments = []
        allStudents = StudentsTable.objects.filter()
        assignments = AssignmentTeacherSide.objects.all()


        for group in request.user.groups.all():
            studentAvailableAssignments.append(group.name)

        for assign in assignments:
            if assign.section in tempSections:
                teacherAssignments.append(assign)


        validAssignments = []
        presentTime = datetime.now()
        users_in_group = Group.objects.get(name="Student").user_set.all()
        onDemandGroup = Group.objects.get(name="Ondemand").user_set.all()
        allSubmittedAssignments = studentAssignments.objects.filter()
        submittedAssignments = []


        for assignment in assignments:
            for section in studentSections:
                if assignment.dueDate.strftime('%Y-%m-%d %H:%M:%S') > presentTime.strftime('%Y-%m-%d %H:%M:%S'):
                    if assignment.section.name == section.sectionFK.name:
                        validAssignments.append(assignment)
      
        for sections in tempSections:
            tempSectionsList.append(sections)

        for student in allStudents:
            if student.sectionFK in tempSectionsList:
                validStudents.append(student)

        for submittedAssignment in allSubmittedAssignments:
            for tempSection in tempSections:
                if submittedAssignment.assignment.section.name == tempSection.name:
                    submittedAssignments.append(submittedAssignment)
        
        numOfActiveUsers = len(users_in_group) 

        if user in users_in_group and user not in onDemandGroup:
            return render(request, 'accounts/studentHome.html', {"assignments":validAssignments, "numOfActiveUsers": numOfActiveUsers})
        elif user in users_in_group and user in onDemandGroup:
            return render(request, 'accounts/demandHome.html', {"assignments":teacherAssignments, "numOfActiveUsers": numOfActiveUsers, "user":user}) 
        else:
            return render(request, 'accounts/teacherHome.html', {"submittedAssignments": submittedAssignments, "validStudents": validStudents,"assignments": teacherAssignments, "numOfActiveUsers": numOfActiveUsers})

    except User.DoesNotExist:
         return render(request, 'accounts/studentHome.html')


def signup(request):
    getSection = Sections.objects.filter()
    allSection = []
    
    for sec in getSection:
        allSection.append(sec.name)

    allSection.remove("Temp")

    if request.method == 'POST':
        isPasswordValid = (request.POST['password'] == request.POST['password2']) and (len(request.POST['password']) > 7)

        if isPasswordValid:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {"error": "This username is taken!", "allSection": allSection})
            except User.DoesNotExist:
                user = User()
                user.first_name = request.POST['fname']
                user.last_name = request.POST['lname']
                user.email = request.POST['email']
                user.username = request.POST['username']
                keepUsernName = user.username
                keepSectionID = request.POST['classID']
                # user.password = request.POST['password']
                user.set_password(request.POST['password'])
                user.save()

                if request.POST['typeUser'] == "teacher":
                    if request.POST['token'] == "1234":
                        tempTeacher = TeachersTable()
                        tempSections = Sections.objects.get(name='Temp')
                        tempTeacherFK = User.objects.get(username=keepUsernName)
                        tempTeacher.teacherFK = tempTeacherFK
                        tempTeacher.sectionFK = tempSections
                        tempTeacher.save()
                    else:
                        return render(request, 'accounts/signup.html', {"error": "Your token is invalid!", "allSection": allSection})
                elif request.POST['typeUser'] == 'student':
                    tempStudent = StudentsTable()
                    tempSection = Sections.objects.get(name=keepSectionID)
                    tempStudentFK = User.objects.get(username=keepUsernName)
                    tempStudent.studentFK = tempStudentFK
                    tempStudent.sectionFK = tempSection
                    tempStudent.save()
                else:
                    pass

                studentGroup = Group.objects.get(name='Student') 
                teacherGroup = Group.objects.get(name='Teacher')
                demandGroup = Group.objects.get(name='Ondemand')

                if request.POST['typeUser'] == "student":
                    studentGroup.user_set.add(user)
                elif request.POST['typeUser'] == "teacher":
                    teacherGroup.user_set.add(user)
                elif request.POST['typeUser'] == "ondemand":
                    studentGroup.user_set.add(user)
                    demandGroup.user_set.add(user)

                return redirect('home')
        else:
             return render(request, 'accounts/signup.html', {"error": "Invalid password!", "allSection": allSection})
    else:
        return render(request, 'accounts/signup.html', {"allSection": allSection})


def login(request):
    assignments = AssignmentTeacherSide.objects

    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            users_in_group = Group.objects.get(name="Student").user_set.all()

            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {"error":"Username or password is incorrect!"})
    else:
        return render(request, 'accounts/login.html')
        

def logout(request):
    if request.method == 'POST':
        auth.logout(request)

        return redirect('home')