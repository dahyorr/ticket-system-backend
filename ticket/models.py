from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from userAuth.models import User


class Queue(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    PRIORITY_CHOICES = (
        (3, 'Normal'),
        (1, 'Critical'),
        (2, 'High'),
        (4, 'Low'),
        (5, 'Very Low'),
    )

    STATUS_CHOICE = (
        (1, 'Open'),
        (2, 'Closed'),
    )

    title = models.CharField(max_length=255)
    opening_text = models.TextField(blank=False, null=False)
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICE, default=1, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              default=get_user_model(), related_name='owner')
    assigned_users = models.ManyToManyField(User, related_name='assigned_users',)

    def __str__(self):
        return self.title


class Reply(models.Model):
    message = models.TextField(blank=False, null=False)
    ticket = models.ForeignKey(Ticket, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='replies',
                               default=get_user_model(), null=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.message
