from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    """
    Gives model, fields and success_url.
    Also add constrictions login required and permission required.
    """
    model = Course
    fields = ("title", "slug", "subject", "description")
    success_url = reverse_lazy("manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Gives template_name
    """
    template_name = "courses/manage/course/form.html"
