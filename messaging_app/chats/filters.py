import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    conversation = django_filters.NumberFilter(field_name="conversation__id")
    date_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    date_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "date_after", "date_before"]
