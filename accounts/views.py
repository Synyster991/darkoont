from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.validators import validate_email
from django.contrib.auth.models import Group
from assignments.models import AssignmentTeacherSide, studentAssignments
from django.utils import timezone

def home(request):
    try:
        userName = request.user.get_username()
        user = User.objects.get(username=userName)
        assignments = AssignmentTeacherSide.objects.all()
        time = timezone.datetime.now()
        users = User.objects
        users_in_group = Group.objects.get(name="Student").user_set.all()
        validStudents = users_in_group


        if user in users_in_group:
            return render(request, 'accounts/studentHome.html', {"assignments":assignments}) 
        else:
            return render(request, 'accounts/teacherHome.html', {"validStudents": validStudents, "assignments":assignments})

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

                if request.POST['typeUser'] == "student":
                    studentGroup.user_set.add(user)
                else:
                    teacherGroup.user_set.add(user)

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

        return render(request, 'accounts/login.html')