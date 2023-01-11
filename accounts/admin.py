from django.contrib import admin
from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email', 'is_staff', 'is_superuser']
# is_staff : 스태프 권한
# is_superuser:최상위 사용자 권한
# 'website_url','is_active'
