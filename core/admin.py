# from django.contrib import admin
# from .models import Facility, Department

# @admin.register(Facility)
# class FacilityAdmin(admin.ModelAdmin):
#     list_display = ['name', 'location', 'capacity']
#     search_fields = ['name', 'location']

# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'facility', 'head_of_department']
#     list_filter = ['facility']

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'date_of_birth', 'address', 'profile_image')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'date_of_birth', 'address')
        }),
    )