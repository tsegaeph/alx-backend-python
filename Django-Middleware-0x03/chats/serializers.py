from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "sender_name",
            "conversation",
            "message_body",
            "sent_at",
        ]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    num_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "num_messages",
            "created_at",
        ]

    def get_num_messages(self, obj):
        return obj.messages.count()
