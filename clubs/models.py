from django.db import models
from accounts.models import User


class Department(models.Model):
    department_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.department_name


class Club(models.Model):
    club_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # Replaced 'faculty_coordinator_id' with standard ForeignKey
    faculty_coordinator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='coordinated_clubs')
    is_council = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.club_name


class ClubMember(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, default='Member')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'user')  # Prevents duplicate membership
