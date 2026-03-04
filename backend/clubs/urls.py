from django.urls import path
from .views import ClubListView, ClubMemberListView

app_name = 'clubs'

urlpatterns = [
    path('clubs/', ClubListView.as_view(), name='club_list'),
    path('clubs/<int:club_id>/members/', ClubMemberListView.as_view(), name='club_members'),
]