from django.db import models


class Event(models.Model):
    """
    Represents an event organized by a club, council, or department.
    Events go through an approval workflow (Proposed → Approved/Rejected → Completed).
    """

    # Choices — must match DB CHECK constraints exactly
    STATUS_CHOICES = [
        ('Proposed', 'Proposed'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Open', 'Open'),          # In DB CHECK constraint
        ('Completed', 'Completed'),
        ('Archived', 'Archived'),  # In DB CHECK constraint
    ]

    ORGANIZER_TYPE_CHOICES = [
        ('Club', 'Club'),
        ('Council', 'Council'),
        ('Department', 'Department'),
    ]

    PARTICIPATION_TYPE_CHOICES = [
        ('Student-only', 'Student-only'),
        ('Faculty-only', 'Faculty-only'),
        ('Joint', 'Joint'),  # DB uses 'Joint', not 'Open'
    ]

    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organizer_type = models.CharField(
        max_length=50,
        choices=ORGANIZER_TYPE_CHOICES  # Enforces valid organizer categories
    )
    club = models.ForeignKey(
        'clubs.Club', on_delete=models.SET_NULL,
        null=True, blank=True,  # Nullable — not all events belong to a club
        db_column='club_id',
        related_name='events'  # Access via club.events.all()
    )
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        db_column='created_by',
        related_name='created_events'  # Access via user.created_events.all()
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Proposed'  # New events start as proposals
    )
    participation_type = models.CharField(
        max_length=50,
        choices=PARTICIPATION_TYPE_CHOICES  # Controls who can register
    )
    max_participants = models.IntegerField(default=0)  # 0 = unlimited
    event_date = models.DateTimeField()

    class Meta:
        db_table = 'Events'

    def __str__(self):
        return f"{self.title} ({self.status})"


class EventApproval(models.Model):
    """
    Weak entity — existence depends on Event (1-to-1 relationship).
    Records the approval/rejection decision for an event proposal.
    """

    DECISION_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # OneToOneField with primary_key=True — this table shares the PK with Event
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE,
        primary_key=True,
        db_column='event_id',
        related_name='approval'  # Access via event.approval
    )
    approved_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='approved_by',
        related_name='approved_events'  # Access via user.approved_events.all()
    )
    approved_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)  # Optional notes from approver
    decision = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES  # Only Approved or Rejected — prevents invalid values
    )

    class Meta:
        db_table = 'Event_Approvals'

    def __str__(self):
        return f"{self.event.title} — {self.decision}"