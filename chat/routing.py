from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # path(r'^ws/chat/(?P<room_name>[^/]+)/(?P<auth>[^/]+)/$', ChatConsumer)
    path("ws/chat/<int:sender_id>/<int:receiver_id>/", consumers.ChatConsumer.as_asgi())
]
