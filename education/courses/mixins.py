from django.urls import reverse_lazy

from .models import Course


class OwnerMixin:
    """
    Mixin return queryset only from recent user
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class OwnerEditMixin:
    """
    Mixin return edit form only for certain user
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    """
    Gives model, fields and success_url
    """
    model = Course
    fields = ("title", "slug", "subject", "description")
    success_url = reverse_lazy('manage_course_list')
