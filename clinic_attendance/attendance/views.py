# attendance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import User, Attendance
from .forms import StaffRegistrationForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"Attempting login for username: {username} with password: {password}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Authenticated user: {user.username}")
            login(request, user)
            if user.is_superuser:
                print("Redirecting superuser to dashboard")
                return redirect('dashboard')
            else:
                print("Redirecting staff member to check-in")
                return redirect('check_in')
        else:
            print("Authentication failed")
    return render(request, 'attendance/login.html')


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('check_in')
    staff_count = User.objects.filter(is_staff_member=True).count()
    today_attendance = Attendance.objects.filter(check_in_time__date=timezone.now().date()).count()
    context = {
        'staff_count': staff_count,
        'today_attendance': today_attendance,
    }
    return render(request, 'attendance/dashboard.html', context)

@login_required
def staff_list(request):
    if not request.user.is_superuser:
        return redirect('check_in')
    staff = User.objects.filter(is_staff_member=True)
    return render(request, 'attendance/staff_list.html', {'staff': staff})

@login_required
def check_in(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        Attendance.objects.create(user=request.user)
        return redirect('check_in')
    today_attendance = Attendance.objects.filter(user=request.user, check_in_time__date=timezone.now().date()).first()
    return render(request, 'attendance/check_in.html', {'today_attendance': today_attendance})

@login_required
def add_staff(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffRegistrationForm()
    return render(request, 'attendance/add_staff.html', {'form': form})


@login_required
def delete_staff(request, staff_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    staff = get_object_or_404(User, id=staff_id)
    staff.delete()
    return redirect('staff_list')


@login_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(User, id=staff_id)
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffRegistrationForm(instance=staff)

    return render(request, 'attendance/edit_staff.html', {'form': form})


@login_required
def change_password(request):
    return PasswordChangeView.as_view(
        template_name='attendance/change_password.html',
        success_url=reverse_lazy('password_change_done')
    )(request)