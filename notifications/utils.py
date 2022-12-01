from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification, APNSConfig, APNSPayload, Aps


def send_notification(user_ids, title, body, image=None, data=None):
    try:
        device = FCMDevice.objects.filter(user__in=user_ids)
        # ios push notification sound and badge
        payload_ = APNSPayload(aps=Aps(badge=1, sound='default'))
        apns_ = APNSConfig(payload=payload_)
        if data:
            device.send_message(Message(notification=Notification(title=title, body=body), data=data, apns=apns_))
    except Exception as e:
        print('exception', e)
