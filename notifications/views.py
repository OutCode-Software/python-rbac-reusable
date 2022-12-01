from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from fcm_django.models import FCMDevice
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import DEVICE_TYPES
from .serializers import FCMDeviceSerializer, PushNotificationSerializer


class FCMDeviceViewSet(APIView):
    """
    Update the push notifications token

    Add the push notification of the user for that device.
    Push notification is sent to that device
    When logged out from that device, the fcm token is deleted
    """

    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']
    parser_classes = [JSONParser, ]

    deviceid = openapi.Parameter('deviceid', in_=openapi.IN_HEADER, description='Unique device Id',
                                 type=openapi.TYPE_STRING)
    devicetype = openapi.Parameter('devicetype', in_=openapi.IN_HEADER, description='Device Type',
                                   type=openapi.TYPE_STRING, enum=DEVICE_TYPES)

    @swagger_auto_schema(manual_parameters=[deviceid, devicetype], request_body=FCMDeviceSerializer,
                         operation_id="update_push_notification_token", responses={status.HTTP_200_OK: "Success"})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status_code': status.HTTP_200_OK,
            'message': 'Success.'
        })


class NotificationViewSet(APIView):
    """
    to send notification to users

    Push notification is sent users
    """
    serializer_class = PushNotificationSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['post']

    @swagger_auto_schema(request_body=PushNotificationSerializer, operation_id="add_notification",
                         responses={status.HTTP_200_OK: "Success"})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # send_notification([], "Message", "Content")  # send notification with this function

        return Response({
            'status_code': status.HTTP_200_OK,
            'message': 'Success.',
            'data': 'Notification Sent ',
        })
