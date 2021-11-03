from rest_framework import serializers
from .models import Queue, Ticket, Reply
from userAuth.models import User


class QueueSerializer(serializers.ModelSerializer):
    """Serializer for Queues"""

    class Meta:
        model = Queue
        fields = ('id', 'title')
        read_only_fields = ('id',)


class ReplySerializer(serializers.ModelSerializer):
    """Serializer for Replies"""
    author = serializers.StringRelatedField()

    class Meta:
        model = Reply
        fields = ('message', 'ticket', 'date', 'author')
        read_only_fields = ('id', 'date', 'author')


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Tickets"""
    status = serializers.ChoiceField(choices=Ticket.STATUS_CHOICE, required=False)
    priority = serializers.ChoiceField(choices=Ticket.PRIORITY_CHOICES)
    owner = serializers.StringRelatedField()
    queue = serializers.PrimaryKeyRelatedField(queryset=Queue.objects.all())
    assigned_users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    replies = ReplySerializer(many=True, read_only=True)

    def to_representation(self, instance):
        """to_representation Return of custom serialized data"""
        data = super().to_representation(instance)
        data.update(status=instance.get_status_display())
        data.update(priority=instance.get_priority_display())
        return data

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'opening_text', 'queue', 'priority', 'status', 'owner',
                  'assigned_users', 'created_date', 'last_updated', 'replies')
        read_only_fields = ('id', 'created_date', 'last_updated', 'owner', 'replies')


class TicketUpdateSerializer(TicketSerializer):
    """Serializer for Tickets Updates"""
    class Meta:
        model = Ticket
        fields = ('id', 'title', 'opening_text', 'queue', 'priority', 'status', 'owner',
                  'assigned_users', 'created_date', 'last_updated', 'replies')
        read_only_fields = ('id', 'opening_text', 'created_date', 'last_updated', 'owner', 'replies')
