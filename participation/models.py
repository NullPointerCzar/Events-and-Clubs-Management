from django.db import models


class EventRegistration(models.Model):
    """
    Tracks user registrations for events.
    A user can register for an event only once (enforced by unique_together).
    """
    event = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE,
        db_column='event_id',
        related_name='registrations'  # Access via event.registrations.all()
    )
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        db_column='user_id',
        related_name='event_registrations'  # Access via user.event_registrations.all()
    )
    registered_at = models.DateTimeField(auto_now_add=True)  # Auto-set on creation

    class Meta:
        db_table = 'Event_Registrations'
        unique_together = (('event', 'user'),)  # Prevents duplicate registrations

    def __str__(self):
        return f"{self.user.full_name} → {self.event.title}"


class Attendance(models.Model):
    """
    Records attendance for events.
    Separate from registration — a user can register but not attend.
    """
    event = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE,
        db_column='event_id',
        related_name='attendance_records'  # Access via event.attendance_records.all()
    )
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        db_column='user_id',
        related_name='attendance_records'  # Access via user.attendance_records.all()
    )
    present = models.BooleanField(default=False)  # True = attended, False = absent
    marked_at = models.DateTimeField(auto_now_add=True)  # When attendance was recorded

    class Meta:
        db_table = 'Attendance'
        unique_together = (('event', 'user'),)  # One attendance record per user per event

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.user.full_name} — {self.event.title} ({status})"