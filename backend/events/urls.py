from django.urls import path
from .views import (
    ProposeEventView,
    MyClubsView,
    FacultyProposedEventsView,
    ReviewEventView,
)

app_name = 'events'

urlpatterns = [
    path('events/propose/', ProposeEventView.as_view(), name='propose_event'),
    path('events/review/', FacultyProposedEventsView.as_view(), name='faculty_events'),
    path('events/<int:event_id>/review/', ReviewEventView.as_view(), name='review_event'),
    path('clubs/my/', MyClubsView.as_view(), name='my_clubs'),
]
