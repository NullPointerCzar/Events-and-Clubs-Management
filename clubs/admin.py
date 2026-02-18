from django.contrib import admin
from .models import Department, Faculty, Club, ClubMember


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name')
    search_fields = ('department_name',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin for Faculty — specialization/subtype of User."""
    list_display = ('id', 'department', 'designation')
    list_filter = ('department', 'designation')
    search_fields = ('id__full_name', 'designation')  # Search by user's name


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'club_name', 'faculty_coordinator', 'is_council')
    list_filter = ('is_council',)  # Filter by club vs council
    search_fields = ('club_name',)


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('club', 'user', 'position', 'joined_at')
    list_filter = ('position', 'club')  # Filter by position or club
    search_fields = ('user__full_name', 'club__club_name')  # Search across FK fields
