from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.utils import timezone
from .models import OTP
from .forms import RegisterForm, LoginForm, OTPForm
import random

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                user = User.objects.create_user(
                    username=email, email=email, 
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['name']
                )
                user.is_active = False  # Require OTP validation
                user.save()
                otp_code = generate_otp()
                OTP.objects.create(user=user, code=otp_code)
                send_mail(
                    "Your OTP Code",
                    f"Your OTP code is {otp_code}",
                    None,
                    [email],
                    fail_silently=False,
                )
                request.session['pending_user'] = user.id
                return redirect('otp_verify')
        else:
            messages.error(request, 'Please fix errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def otp_verify(request):
    pending_user_id = request.session.get('pending_user')
    if not pending_user_id:
        return redirect('register')
    user = User.objects.get(id=pending_user_id)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            try:
                otp_obj = OTP.objects.filter(user=user, code=otp_code, is_used=False).latest('created_at')
                if (timezone.now() - otp_obj.created_at).seconds > 600:  # 10 min expiry
                    messages.error(request, 'OTP expired. Please register again.')
                    user.delete()
                    return redirect('register')
                otp_obj.is_used = True
                otp_obj.save()
                user.is_active = True
                user.save()
                auth.login(request, user)
                del request.session['pending_user']
                return redirect('homepage')
            except OTP.DoesNotExist:
                messages.error(request, 'Invalid OTP.')
    else:
        form = OTPForm()
    return render(request, 'accounts/otp_verify.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=email, password=password)
            if user:
                otp_code = generate_otp()
                OTP.objects.create(user=user, code=otp_code)
                send_mail(
                    "Your OTP Code",
                    f"Your OTP code is {otp_code}",
                    None,
                    [email],
                    fail_silently=False,
                )
                request.session['login_user'] = user.id
                return redirect('login_otp')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def login_otp(request):
    user_id = request.session.get('login_user')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            try:
                otp_obj = OTP.objects.filter(user=user, code=otp_code, is_used=False).latest('created_at')
                if (timezone.now() - otp_obj.created_at).seconds > 600:
                    messages.error(request, 'OTP expired. Please login again.')
                    return redirect('login')
                otp_obj.is_used = True
                otp_obj.save()
                auth.login(request, user)
                del request.session['login_user']
                return redirect('homepage')
            except OTP.DoesNotExist:
                messages.error(request, 'Invalid OTP.')
    else:
        form = OTPForm()
    return render(request, 'accounts/otp_verify.html', {'form': form})

def logout_view(request):
    auth.logout(request)
    return redirect('login')
