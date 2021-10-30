from django.utils import  timezone
from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Queue, Ticket, Reply
from ticket import serializers
from .notify import send_ticket_reply_notification, send_ticket_created_notification, \
    send_ticket_updated_notification


class IsAdminOrUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_active:
            return True
        else:
            return request.user.is_staff


class IsAuthorizedOrUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_active:
            return True
        elif request.method in ['DELETE', 'PUT'] and request.user.is_superuser:
            return True

        else:
            if hasattr(request.user, 'is_authorized'):
                return request.user.is_authorized
            else:
                return False


class QueueViewSet(viewsets.ModelViewSet):
    """Manage queues in the database"""
    permission_classes = (IsAdminOrUserReadOnly,)
    queryset = Queue.objects.all()
    serializer_class = serializers.QueueSerializer

    def get_queryset(self):
        """return objects by id"""
        return self.queryset.filter().order_by('title')


class TicketViewSet(viewsets.ModelViewSet):
    """Manage queues in the database"""
    permission_classes = (IsAuthorizedOrUserReadOnly,)
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']

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
        user = self.request.user
        ticket = serializer.save(owner=user)
        users = ticket.assigned_users.all().exclude(id=user.id)
        for user in users:
            send_ticket_created_notification(user.id, user, ticket.id)

    def perform_update(self, serializer):
        user = self.request.user
        ticket = serializer.save(last_updated=timezone.now())
        users = ticket.assigned_users.all().exclude(id=user.id)
        for user in users:
            send_ticket_updated_notification(user.id, user, ticket.id)




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
        for user in users:
            send_ticket_reply_notification(user.id, user, ticket_id)
