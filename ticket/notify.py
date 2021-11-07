from .models import Notification
from django.contrib.auth import get_user_model

user = get_user_model().objects.get(email='dahyor@outlook.com')

def send_ticket_created_notification( owner, ticket_id, users):
    content = f'{owner} created a new ticket #{ticket_id} and assigned it to you'
    notification = Notification(content=content, type='Create Ticket')
    notification.save()
    notification.users.set(users)

def send_ticket_reply_notification(from_user, ticket_id, users):
    content = f'{from_user} sent a reply on ticket #{ticket_id}'
    notification = Notification(content=content, type='Reply Ticket')
    notification.save()
    notification.users.set(users)

def send_ticket_updated_notification(by_user, ticket_id, users):
    content = f'Ticket #{ticket_id} was updated by {by_user}'
    notification = Notification(content=content, type='Update Ticket')
    notification.save()
    notification.users.set(users)
