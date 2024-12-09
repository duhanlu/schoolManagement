from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .forms import LoginForm
from teachers.models import Teacher
# Create your views here.
def user_login(request):
    # check if it is a post request
    if request.method == 'POST':
        # form validation
        form = LoginForm(data=request.POST)
        if not form.is_valid():
            return JsonResponse({'status': 'error', 'messages': 'Submition error'}, status=404)
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')

         # check role
        if role == 'teacher':
            try: 
                teacher = Teacher.objects.get(phone_number=username)
                username = teacher.teacher_name + '_' + teacher.phone_number
                user = authenticate(username=username, password=password)
            except:
                return JsonResponse({'status': 'error', 'messages': 'Teacher does not exist'}, status=400)
        elif role == 'student':
            try: 
                student = Student.objects.get(student_number=username)
                username = student.student_name + '_' + student.student_number
                user = authenticate(username=username, password=password)
            except: 
                return JsonResponse({'status': 'error', 'messages': 'Student does not exist'}, status=404)
        else:
            try:
                user = authenticate(username=username, password=password)
            except:
                return JsonResponse({'status': 'error', 'messages': 'Manager information does not exist'} , status=404)

        # return json data after validation
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username.split('_')[0]
                request.session['user_role'] = role
                return JsonResponse({'status': 'success', 'messages': 'Login successfully', 'role': role})
            else: 
                return JsonResponse({'status': 'error', 'messages': 'Unactive account'}, status=403)
        else:
            return JsonResponse({'status': 'error', 'messages': 'Incorrect username or password'}, status=403)





    return render(request, 'accounts/login.html')

def user_logout(request):
    if 'user_role' in request.session:
        del request.session['user_role']
    logout(request)
    request.session.flush()
    return redirect('user_login')

def change_password(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            return JsonResponse({
                'status': 'success',
                'messages': 'Password is changed successfully',
            })
        else:
            errors = form.errors.as_json()
            return JsonResponse({
                'status': 'error',
                'messages': errors,
            })
    return render(request, 'accounts/change_password.html')