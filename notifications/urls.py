from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import FCMDeviceViewSet, NotificationViewSet

router = SimpleRouter()
app_name = "push_notification"
urlpatterns = router.urls
urlpatterns += [
    path('set-fcm-token/', FCMDeviceViewSet.as_view()),
    path('notification/send/', NotificationViewSet.as_view()),
]
