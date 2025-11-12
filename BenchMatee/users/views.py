from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from users.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
        return render(request, 'users/index.html')


def login_register_view(request):
    form_type = 'login'  

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            form_type = 'login'
            login_form = AuthenticationForm(request, data=request.POST)
            register_form = RegisterForm()
            
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        
        elif 'register_submit' in request.POST:
            form_type = 'register'
            register_form = RegisterForm(request.POST)
            login_form = AuthenticationForm()
            
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')  
            else:
                messages.error(request, "Please correct the errors below.")

    else:
        login_form = AuthenticationForm()
        register_form = RegisterForm()

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'form_type': form_type
    }
    return render(request, 'users/login.html', context)


@login_required
def profile(request):
    username = request.user.username
    email = request.user.email
    context = {
        'username': username,
        'email': email
    }
    return render(request, 'users/profile.html', context)

