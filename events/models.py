from django.db import models

# Create your models here.

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organizer_type = models.CharField(max_length=50) # 'Club', 'Council', 'Department'
    club = models.ForeignKey('clubs.Club', on_delete=models.SET_NULL, null=True, db_column='club_id')
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='created_by')
    status = models.CharField(max_length=50, default='Proposed')
    participation_type = models.CharField(max_length=50) # 'Student-only', etc.
    max_participants = models.IntegerField(default=0)
    event_date = models.DateTimeField()

    class Meta:
        db_table = 'Events'

class EventApproval(models.Model):
    # Weak entity: 1-to-1 with Event
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True, db_column='event_id')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, db_column='approved_by')
    approved_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    decision = models.CharField(max_length=20)

    class Meta:
        db_table = 'Event_Approvals'