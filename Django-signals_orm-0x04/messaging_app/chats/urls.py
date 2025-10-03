# messaging_app/chats/urls.py
from django.urls import path
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet, cached_messages_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Main router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages inside conversations
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# JWT Authentication endpoints
urlpatterns = [
    # Include router URLs
    *router.urls,
    *conversation_router.urls,

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("cached-messages/", cached_messages_view, name="cached-messages"),
]
