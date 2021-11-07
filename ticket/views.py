from django.utils import timezone
from rest_framework import viewsets, mixins
from .models import Queue, Ticket, Reply, Notification
from .permissions import IsAdminOrUserReadOnly, IsAuthorizedOrUserReadOnly
from ticket import serializers
from .notify import (send_ticket_created_notification, 
                    send_ticket_reply_notification, 
                    send_ticket_updated_notification)


class QueueViewSet(viewsets.ModelViewSet):
    """Manage queues in the database"""
    permission_classes = (IsAdminOrUserReadOnly,)
    queryset = Queue.objects.all()
    serializer_class = serializers.QueueSerializer

    def get_queryset(self):
        """return objects by id"""
        return self.queryset.filter().order_by('title')


class TicketViewSet(viewsets.ModelViewSet):
    """Manage tickets in the database"""
    permission_classes = (IsAuthorizedOrUserReadOnly,)
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return serializers.TicketUpdateSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        status = self.request.query_params.get('status')
        user = self.request.query_params.get('user')
        if status:
            queryset = queryset.filter(status=status)
        if user and bool(int(user)):
            queryset = queryset.filter(owner=self.request.user.id)
        return queryset.order_by('-created_date')

    def perform_create(self, serializer):
        """create a new Ticket"""
        owner = self.request.user
        ticket = serializer.save(owner=owner)
        users = ticket.assigned_users.all().exclude(id=owner.id)
        send_ticket_created_notification( owner, ticket.id, users)

    def perform_update(self, serializer):
        user = self.request.user
        ticket = serializer.save(last_updated=timezone.now())
        users = ticket.assigned_users.all().exclude(id=user.id)
        send_ticket_updated_notification(user, ticket.id, users)


class ReplyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,):
    """Manage queues in the database"""
    permission_classes = (IsAuthorizedOrUserReadOnly,)
    queryset = Reply.objects.all()
    serializer_class = serializers.ReplySerializer

    def get_queryset(self):
        """return objects by id"""
        return self.queryset.order_by('date')

    def perform_create(self, serializer):
        """create a new Reply"""
        user = self.request.user
        reply = serializer.save(author=user)
        ticket_id = reply.ticket.id
        users = Ticket.objects.get(id=ticket_id).assigned_users.all().exclude(id=user.id)
        send_ticket_reply_notification(user, ticket_id, users)

class NotificationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage queues in the database"""
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        """return objects by id"""
        all = self.request.query_params.get('all')
        if all:
            return self.request.user.notifications.all().order_by('-date')
        else:
            return self.request.user.notifications.all().order_by('-date')[:10]
    
