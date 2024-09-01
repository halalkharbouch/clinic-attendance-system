# attendance/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordChangeView
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff-list/', views.staff_list, name='staff_list'),
    path('check-in/', views.check_in, name='check_in'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('edit-staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='attendance/change_password.html',
        success_url='/password-change/done/'
    ), name='change_password'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='attendance/password_change_done.html'
    ), name='password_change_done'),

]

# Ensure logout only accepts POST requests
from django.views.decorators.http import require_http_methods
urlpatterns += [
    path('logout/', require_http_methods(["POST"])(LogoutView.as_view()), name='logout'),
]