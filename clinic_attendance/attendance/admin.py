# attendance/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Attendance

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_staff_member', 'department', 'staff_number']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_staff_member', 'department', 'staff_number')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Attendance)