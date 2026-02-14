from django.db import models

# Create your models here.

class EventRegistration(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, db_column='event_id')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='user_id')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Event_Registrations'
        unique_together = (('event', 'user'),)

class Attendance(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, db_column='event_id')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='user_id')
    present = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Attendance'
        unique_together = (('event', 'user'),)