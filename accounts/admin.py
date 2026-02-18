from django.contrib import admin
from .models import User, Role, UserRole


# Register models so they appear in the Django admin panel (http://localhost:8000/admin/)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin config for User — controls what columns and filters appear."""
    list_display = ('id', 'full_name', 'email', 'user_type', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active')  # Sidebar filters
    search_fields = ('full_name', 'email')  # Search bar fields
    ordering = ('-created_at',)  # Newest first


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name')
    search_fields = ('role_name',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
