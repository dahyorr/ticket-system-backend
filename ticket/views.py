from rest_framework import viewsets, mixins
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Queue, Ticket, Reply
from ticket import serializers


class IsAdminOrUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        print('rrr')
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


class QueueViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    """Manage queues in the database"""
    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication)
    permission_classes = (IsAdminOrUserReadOnly,)
    queryset = Queue.objects.all()
    serializer_class = serializers.QueueSerializer

    def get_queryset(self):
        """return objects by id"""
        return self.queryset.filter().order_by('title')

    def perform_create(self, serializer):
        """create a new Queue"""
        serializer.save()


class TicketViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """Manage queues in the database"""

    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication)
    permission_classes = (IsAuthorizedOrUserReadOnly,)
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer

    def get_queryset(self,):
        """return objects by id"""
        # if self.request.user.id == self.queryset.get(pk=1):
        # print(self.request.GET.keys())
        return self.queryset.filter().order_by('-created_date')

    def perform_create(self, serializer):
        """create a new Queue"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        print((self.request.GET))


class ReplyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    """Manage queues in the database"""

    # authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication)
    permission_classes = (IsAuthorizedOrUserReadOnly,)
    queryset = Reply.objects.all()
    serializer_class = serializers.ReplySerializer