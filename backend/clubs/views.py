from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Club, ClubMember
from .serializers import ClubSerializer, ClubMemberSerializer


class ClubListView(generics.ListAPIView):
	queryset = Club.objects.select_related('faculty_coordinator').order_by('club_name')
	serializer_class = ClubSerializer
	permission_classes = [IsAdminUser]


class ClubMemberListView(generics.ListAPIView):
	serializer_class = ClubMemberSerializer
	permission_classes = [IsAdminUser]

	def get_queryset(self):
		club_id = self.kwargs['club_id']
		return ClubMember.objects.select_related('user', 'club').filter(club_id=club_id, user__user_type='Student').order_by('position', 'user__full_name')
