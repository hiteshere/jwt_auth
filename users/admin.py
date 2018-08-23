from django.contrib import admin
from .models import User, Job


class UserJobInline(admin.StackedInline):
    model = Job
    extra = 0
    min_num = 1
    max_num = 1
    verbose_name = 'User job details'
    verbose_name_plural = 'User job details'
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    inlines = [UserJobInline]
    exclude = ('groups', 'user_permissions', 'is_superuser')
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_delete', 'date_joined')

admin.site.register(User, UserAdmin)
admin.site.register(Job)
