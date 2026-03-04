from rest_framework import serializers
from .models import Event, EventApproval


class EventSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.full_name', read_only=True
    )
    club_name = serializers.CharField(
        source='club.club_name', read_only=True
    )

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'organizer_type',
            'club',
            'club_name',
            'created_by',
            'created_by_name',
            'status',
            'event_date',
            'created_at',
        ]
        read_only_fields = ['created_by', 'status', 'created_at', 'organizer_type']


class EventApprovalSerializer(serializers.ModelSerializer):
    approved_by_name = serializers.CharField(
        source='approved_by.full_name', read_only=True
    )

    class Meta:
        model = EventApproval
        fields = [
            'event',
            'approved_by',
            'approved_by_name',
            'approved_at',
            'remarks',
            'decision',
        ]
        read_only_fields = ['event', 'approved_by', 'approved_at']
