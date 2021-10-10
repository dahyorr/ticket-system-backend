import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from userAuth.models import User

# Create your models here.
date = datetime.date.today()


class Queue(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    PRIORITY_CHOICES = (
        (1, '1. Critical'),
        (2, '2. High'),
        (3, '3. Normal'),
        (4, '4. Low'),
        (5, '5. Very Low'),
    )

    title = models.CharField(max_length=255)
    opening_text = models.TextField(blank=False, null=False)
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3, blank=3,)
    status = models.BooleanField(default=True)  # Ticket status True means ticket is open
    created_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              default=get_user_model(), related_name='owner')
    assigned_users = models.ManyToManyField(User, related_name='assigned_users',)
    ticket_date = models.IntegerField(default=int(f'{date.year}{date.month:02}{date.day:02}'))

    def __str__(self):
        return self.title


class Reply(models.Model):
    message = models.TextField(blank=False, null=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=get_user_model())
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'
