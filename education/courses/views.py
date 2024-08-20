from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView

from .forms import ModuleFormSet
from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Course


class CourseManageListView(ListView):
    """
    View for manage courses by the author
    """
    model = Course
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"

    def get_queryset(self):
        """
        return: queryset of author's courses
        """
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = "courses.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = "courses.change_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"


class CourseAndModuleUpdateView(TemplateResponseMixin, View):
    """
    This class manage addition, updating and deleting of certain course modules
    """
    template_name = "courses/manage/formset.html"
    course = None

    def get_formset(self, data=None):
        """Get form ModuleFormSet and fill in it with data"""
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, id):
        """
        Send request to methods get or post.
        Get model Course with recent user.
        Save parameter "course" for other methods
        """
        self.course = get_object_or_404(Course, id=id, author=request.user)
        return super().dispatch(request, id)

    def get(self, request, *args, **kwargs):
        """Return ana empty form and template with certain context"""
        formset = self.get_formset()
        return self.render_to_response({"course": self.course, "formset": formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_course_list")
        return self.render_to_response({"course": self.course, "formset": formset})
