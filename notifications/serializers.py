from fcm_django.models import FCMDevice
from rest_framework import serializers
from .models import Notification

class FCMDeviceSerializer(serializers.ModelSerializer):
    token = serializers.CharField(style={'base_template': 'textarea.html'}, required=True)

    class Meta:
        model = FCMDevice
        fields = ['token', ]

    def validate(self, data):
        return data

    def create(self, validated_data):
        device_id = self.context['request'].headers.get('deviceid', '')
        device_type = self.context['request'].headers.get('devicetype', '')
        registration_id = validated_data.get('token')
        user = self.context['request'].user
        FCMDevice.objects.filter(device_id=device_id).delete()
        data = {
            "device_id": device_id,
            "user": user,
            "registration_id": registration_id,
            "type": device_type,
            "name": user.full_name,
            "active": 1,
        }
        device = FCMDevice.objects.create(**data)
        return device


class PushNotificationSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.UUIDField(), allow_null=False)
    title = serializers.CharField(allow_blank=False)
    body = serializers.CharField(allow_blank=True)
    image = serializers.ImageField(allow_null=True, required=False)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids')
        notification = Notification.objects.create(sent_by_id=self.context['user'].id, **validated_data)
        notification.save()
        if user_ids is not None:
            notification.users.set(user_ids)

        return notification
