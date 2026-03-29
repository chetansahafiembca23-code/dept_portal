from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def register_view(request):
    if request.method == 'POST':
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        r = request.POST['roll']
        
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already taken")
            return redirect('register')
            
        user = User.objects.create_user(username=u, email=e, password=p, roll_number=r)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('dashboard')
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('name')
        user.phone_number = request.POST.get('phone')
        user.college_email = request.POST.get('email')
        user.department = request.POST.get('department')
        user.is_profile_complete = True  # Mark as complete!
        user.save()
        
        messages.success(request, "Profile updated! You can now enroll in events.")
        return redirect('home')  # Send them back to the main dashboard
        
    return render(request, 'users/profile_update.html')