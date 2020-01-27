from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.validators import validate_email
from django.contrib.auth.models import Group

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
                user.password = request.POST['password']

                user.save()

                studentGroup = Group.objects.get(name='Student') 
                teacherGroup = Group.objects.get(name='Teacher')

                if request.POST['typeUser'] == "student":
                    studentGroup.user_set.add(user)
                else:
                    teacherGroup.user_set.add(user)

                auth.login(request, user)

                return redirect('signup')
        else:
             return render(request, 'accounts/signup.html', {"error": "Invalid password!"})
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    return(render(request, 'accounts/login.html'))