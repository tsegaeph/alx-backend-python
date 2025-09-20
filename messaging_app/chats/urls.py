from rest_framework import routers
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Create router instance exactly using routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
