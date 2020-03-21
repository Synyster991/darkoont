from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group
from assignments.models import AssignmentTeacherSide, studentAssignments, Sections
from accounts.models import TeachersTable, StudentsTable
from datetime import datetime

def home(request):
    try:
        # Retriving data from database
        userName = request.user.get_username()
        user = User.objects.get(username=userName)
        tempSections = Sections.objects.filter(owner=user)
        studentSections = StudentsTable.objects.filter(studentFK=user)
        allStudents = StudentsTable.objects.filter()
        assignments = AssignmentTeacherSide.objects.all()
        allSubmittedAssignments = studentAssignments.objects.filter()

        # Empty lists to insert validated data
        validStudents = []
        validAssignments = []
        tempSectionsList = []
        teacherAssignments = []
        submittedAssignments = []      
        renderStudentSections = []
        
        # Get only student users
        users_in_group = Group.objects.get(name="Student").user_set.all()

        presentTime = datetime.now()
        
        # Making sure that teacher will se only their assignments
        for assign in assignments:
            if assign.section in tempSections:
                teacherAssignments.append(assign)

        for asd in studentSections:
            renderStudentSections.append(asd)

        # Checking the right section and due date for student's assignments
        for assignment in assignments:
            for section in studentSections:
                if assignment.dueDate.strftime('%Y-%m-%d %H:%M:%S') > presentTime.strftime('%Y-%m-%d %H:%M:%S'):
                    if assignment.section.name == section.sectionFK.name:
                        validAssignments.append(assignment)
      
        # Converting Query to List of sections name
        for sections in tempSections:
            tempSectionsList.append(sections)

        # Making sure teachers will see their students
        for student in allStudents:
            if student.sectionFK in tempSectionsList:
                validStudents.append(student)

        # See Recent submission, but only for their students
        for submittedAssignment in allSubmittedAssignments:
            for tempSection in tempSections:
                if submittedAssignment.assignment.section.name == tempSection.name:
                    submittedAssignments.append(submittedAssignment)
        
        # Checking if the logged in user is student or teacher
        if user in users_in_group:
            return render(request, 'accounts/studentHome.html', {"assignments":validAssignments, "studentSections": renderStudentSections})
        else:
            return render(request, 'accounts/teacherHome.html', {"submittedAssignments": submittedAssignments, "validStudents": validStudents, "assignments": teacherAssignments, "sections": tempSections})

    except User.DoesNotExist:
         return render(request, 'accounts/studentHome.html')


def signup(request):
    # Creating list of Section's name from query
    getSection = Sections.objects.filter()
    allSection = []
    
    for sec in getSection:
        if sec.public:
            allSection.append(sec.name)

    # Creating new user
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
                    if request.POST['token'] == "1234": # TODO - change it with local_settings.py
                        tempTeacher = TeachersTable()
                        tempSections = Sections.objects.get(name='GoingPrivate')
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

                # Seperating students and teachers
                studentGroup = Group.objects.get(name='Student') 
                teacherGroup = Group.objects.get(name='Teacher')

                if request.POST['typeUser'] == "student":
                    studentGroup.user_set.add(user)
                elif request.POST['typeUser'] == "teacher":
                    teacherGroup.user_set.add(user)
 
                return redirect('home')
        else:
             return render(request, 'accounts/signup.html', {"error": "Invalid password!", "allSection": allSection})
    else:
        return render(request, 'accounts/signup.html', {"allSection": allSection})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
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