from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notification_over_socket(group_name, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, data)


def send_ticket_reply_notification(user_id, from_user, ticket_id):
    group_name = str(user_id)
    time = str(datetime.now().isoformat())
    data = {
        "type": 'send_notification',
        "text": {
            "message": f'{from_user} sent a reply on ticket #{ticket_id}',
            "time": time
        }
    }
    send_notification_over_socket(group_name, data)


def send_ticket_created_notification(user_id, owner, ticket_id):
    group_name = str(user_id)
    time = str(datetime.now().isoformat())
    data = {
        "type": 'send_notification',
        "text": {
            "message": f'{owner} created a new ticket #{ticket_id} and assigned you to it',
            "time": time
        }
    }
    send_notification_over_socket(group_name, data)


def send_ticket_updated_notification(user_id, from_user, ticket_id):
    group_name = str(user_id)
    time = str(datetime.now().isoformat())
    data = {
        "type": 'send_notification',
        "text": {
            "message": f'{from_user} made an update to ticket #{ticket_id}',
            "time": time
        }
    }
    send_notification_over_socket(group_name, data)
