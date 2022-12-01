from notifications.utils import send_notification
from notifications.models import Notification
from .models import User

#Adjust Notification according to the Need

def on_state_change_push_notification(user, title, body):
    data = {'title': title, 'body': body}
    user_ids = User.objects.filter(is_superuser=False).exclude(id=user.id).values_list('id', flat=True)
    notification = Notification.objects.create(title=title, body=body, sent_by=user)
    notification.users.set(user_ids)
    send_notification(user_ids, title, body, image=None, data=data)