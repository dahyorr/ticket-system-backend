from rest_framework import serializers
from .models import Queue, Ticket, Reply


class QueueSerializer(serializers.ModelSerializer):
    """Serializer for Queues"""

    class Meta:
        model = Queue
        fields = ('id', 'title')
        read_only_fields = ('id',)


class ReplySerializer(serializers.ModelSerializer):
    """Serializer for Replies"""

    class Meta:
        model = Reply
        fields = ('id', 'message', 'ticket', 'date')
        read_only_fields = ('id', 'date')


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Tickets"""

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'opening_text', 'queue', 'priority', 'status', 'owner',
                  'assigned_users', 'created_date')
        read_only_fields = ('id', 'created_date')
