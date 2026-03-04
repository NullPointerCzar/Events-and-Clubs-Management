from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Event, EventApproval
from .serializers import EventSerializer, EventApprovalSerializer
from clubs.models import Club, ClubMember


class ProposeEventView(generics.CreateAPIView):
    """
    Club members (event managers) can propose an event for their club.
    Only students who are members of the given club can propose.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        club = serializer.validated_data.get('club')
        user = self.request.user

        # Ensure the user is an Event Manager in the club
        if not ClubMember.objects.filter(club=club, user=user, position='Event Manager').exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only Event Managers of this club can propose events.')

        serializer.save(
            created_by=user,
            organizer_type='Club',
            status='Proposed',
        )


class MyClubsView(generics.ListAPIView):
    """
    Returns the clubs the current student is a member of 
    (so they can choose which club to propose events for).
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        memberships = ClubMember.objects.select_related('club').filter(
            user=request.user, position='Event Manager'
        ).order_by('club__club_name')
        data = [
            {
                'club_id': m.club.id,
                'club_name': m.club.club_name,
                'position': m.position,
            }
            for m in memberships
        ]
        return Response(data)



class FacultyProposedEventsView(generics.ListAPIView):
    """
    Lists proposed events.
    - Admin: sees ALL proposed events across every club.
    - Faculty coordinator (HoD): sees proposed events only for their clubs.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Admin can see all proposed events
        if user.is_staff or user.user_type == 'Admin':
            return Event.objects.select_related('club', 'created_by').filter(
                status='Proposed',
            ).order_by('-created_at')

        # Faculty coordinator sees only their clubs' proposals
        coordinated_clubs = Club.objects.filter(
            faculty_coordinator=user
        )
        return Event.objects.select_related('club', 'created_by').filter(
            club__in=coordinated_clubs,
            status='Proposed',
        ).order_by('-created_at')


class ReviewEventView(APIView):
    """
    Faculty coordinator (HoD) can approve or reject a proposed event.
    POST body: { "decision": "Approved" | "Rejected", "remarks": "..." }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)

        # Admin can review any event; faculty must be the coordinator
        is_admin = request.user.is_staff or request.user.user_type == 'Admin'
        is_coordinator = event.club and event.club.faculty_coordinator == request.user

        if not is_admin and not is_coordinator:
            return Response(
                {'detail': 'You are not authorised to review this event.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if event.status != 'Proposed':
            return Response(
                {'detail': 'This event has already been reviewed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        decision = request.data.get('decision')
        if decision not in ('Approved', 'Rejected'):
            return Response(
                {'detail': 'Decision must be "Approved" or "Rejected".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        remarks = request.data.get('remarks', '')

        # Update event status
        event.status = decision
        event.save()

        # Create approval record
        EventApproval.objects.create(
            event=event,
            approved_by=request.user,
            decision=decision,
            remarks=remarks,
        )

        return Response({
            'detail': f'Event {decision.lower()} successfully.',
            'event_id': event.id,
            'status': event.status,
        })
