from django.db import models

# Create your models here.

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'Departments'

class Club(models.Model):
    club_id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    faculty_coordinator_id = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, db_column='faculty_coordinator_id')
    is_council = models.BooleanField(default=False)

    class Meta:
        db_table = 'Clubs'
        

class ClubMember(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, db_column='club_id')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='user_id')
    position = models.CharField(max_length=100, default='Member')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Club_Members'
        unique_together = (('club', 'user'),)