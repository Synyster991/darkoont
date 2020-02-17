from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.validators import validate_email
from django.contrib.auth.models import Group
from assignments.models import AssignmentTeacherSide, studentAssignments
from datetime import datetime

def home(request):
    try:
        userName = request.user.get_username()
        user = User.objects.get(username=userName)
        assignments = AssignmentTeacherSide.objects.all()
        validAssignments = []
        presentTime = datetime.now()
        users_in_group = Group.objects.get(name="Student").user_set.all()
        onDemandGroup = Group.objects.get(name="Ondemand").user_set.all()
        validStudents = users_in_group

        for assignment in assignments:
            if assignment.dueDate.strftime('%Y-%m-%d %H:%M:%S') > presentTime.strftime('%Y-%m-%d %H:%M:%S'):
                validAssignments.append(assignment) 

        numOfActiveUsers = len(users_in_group) 

        if user in users_in_group and user not in onDemandGroup:
            return render(request, 'accounts/studentHome.html', {"assignments":validAssignments, "numOfActiveUsers": numOfActiveUsers})
        elif user in users_in_group and user in onDemandGroup:
            return render(request, 'accounts/demandHome.html', {"assignments":validAssignments, "numOfActiveUsers": numOfActiveUsers}) 
        else:
            return render(request, 'accounts/teacherHome.html', {"validStudents": validStudents, "assignments": assignments, "numOfActiveUsers": numOfActiveUsers})

    except User.DoesNotExist:
         return render(request, 'accounts/studentHome.html')


def signup(request):
    if request.method == 'POST':
        isPasswordValid = (request.POST['password'] == request.POST['password2']) and (len(request.POST['password']) > 7)

        if isPasswordValid:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {"error": "This username is taken!"})
            except User.DoesNotExist:
                user = User()
                user.first_name = request.POST['fname']
                user.last_name = request.POST['lname']
                user.email = request.POST['email']
                user.username = request.POST['username']
                # user.password = request.POST['password']
                user.set_password(request.POST['password'])

                if request.POST['typeUser'] == "teacher":
                    if request.POST['token'] == "1234":
                        pass
                    else:
                        return render(request, 'accounts/signup.html', {"error": "Your token is invalid!"})
                else:
                    pass

                user.save()

                studentGroup = Group.objects.get(name='Student') 
                teacherGroup = Group.objects.get(name='Teacher')
                demandGroup = Group.objects.get(name='Ondemand')
                py101Class = Group.objects.get(name='PY101')

                if request.POST['typeUser'] == "student":
                    studentGroup.user_set.add(user)
                    py101Class.user_set.add(user)
                elif request.POST['typeUser'] == "teacher":
                    teacherGroup.user_set.add(user)
                elif request.POST['typeUser'] == "ondemand":
                    studentGroup.user_set.add(user)
                    demandGroup.user_set.add(user)

                return redirect('home')
        else:
             return render(request, 'accounts/signup.html', {"error": "Invalid password!"})
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    assignments = AssignmentTeacherSide.objects
    users_in_group = Group.objects.get(name="Student").user_set.all()

    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            isTeacher = False
            users_in_group = Group.objects.get(name="Student").user_set.all()

            if user in users_in_group:
                isTeacher = False
            else:
                isTeacher = True

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