from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Dummy OTP system for demo!
def send_otp_to_email(email, otp):
    print(f"Send OTP {otp} to {email}")

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        # Set OTP in session
        otp = '123456'
        request.session['otp'] = otp
        request.session['email'] = email
        send_otp_to_email(email, otp)
        return redirect('accounts:otp_verify')
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # If OTP is required, redirect to verify
            if not request.session.get('otp_verified'):
                request.session['email'] = email
                otp = '123456'
                request.session['otp'] = otp
                send_otp_to_email(email, otp)
                return redirect('accounts:otp_verify')
            login(request, user)
            return redirect('homepage:home') # Change to your home url name
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        real_otp = request.session.get('otp')
        if entered_otp == real_otp:
            request.session['otp_verified'] = True
            email = request.session.get('email')
            user = authenticate(request, username=email, password=request.POST.get('password', ''))
            if user:
                login(request, user)
            return redirect('homepage:home') # Change to your home url name
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'accounts/otp_verify.html')
