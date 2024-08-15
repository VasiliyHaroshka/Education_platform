from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Course


class CourseManageListView(ListView):
    """
    View for manage courses by the author
    """
    model = Course
    template_name = "courses/manage/course/list.html"

    def get_queryset(self):
        """
        return: queryset of author's courses
        """
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    ...


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    ...


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
