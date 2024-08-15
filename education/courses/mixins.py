from django.urls import reverse_lazy

from .models import Course


class OwnerMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)



