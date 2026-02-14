from django.db import models


class Department(models.Model):
    """Represents academic departments in the institution."""
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'Departments'

    def __str__(self):
        return self.department_name


class Faculty(models.Model):
    """
    Specialization/Subtype of Users — represents faculty members.
    Maps to the Faculty table in DB which references Users(user_id).
    """
    faculty_id = models.OneToOneField(
        'accounts.User', on_delete=models.CASCADE,
        primary_key=True,  # Shares PK with Users table
        db_column='faculty_id',
        related_name='faculty_profile'  # Access via user.faculty_profile
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='department_id',
        related_name='faculty_members'  # Access via department.faculty_members.all()
    )
    designation = models.CharField(max_length=100, null=True, blank=True)  # e.g., 'Assistant Professor', 'HOD'

    class Meta:
        db_table = 'Faculty'  # Matches DB table name

    def __str__(self):
        return f"{self.faculty_id.full_name} — {self.designation or 'Faculty'}"


class Club(models.Model):
    """
    Represents a student club or council.
    A club can optionally have a faculty coordinator (references Faculty, not User directly).
    """
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    faculty_coordinator_id = models.ForeignKey(
        Faculty,  # DB script: REFERENCES Faculty(faculty_id)
        on_delete=models.SET_NULL,  # Keep club even if coordinator is deleted
        null=True,
        blank=True,  # Allow empty in forms (matches null=True)
        db_column='faculty_coordinator_id',
        related_name='coordinated_clubs'  # Access via faculty.coordinated_clubs.all()
    )
    is_council = models.BooleanField(default=False)  # True if this is a council, not a regular club

    class Meta:
        db_table = 'Clubs'

    def __str__(self):
        return self.club_name


class ClubMember(models.Model):
    """
    Junction table for club membership.
    Tracks which user belongs to which club, their position, and when they joined.
    """
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE,
        db_column='club_id',
        related_name='members'  # Access via club.members.all()
    )
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        db_column='user_id',
        related_name='club_memberships'  # Access via user.club_memberships.all()
    )
    position = models.CharField(max_length=100, default='Member')  # e.g., 'President', 'Secretary'
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Club_Members'
        unique_together = (('club', 'user'),)  # A user can only join a club once

    def __str__(self):
        return f"{self.user.full_name} — {self.club.club_name} ({self.position})"