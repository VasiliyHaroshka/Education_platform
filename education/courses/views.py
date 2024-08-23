from django.apps import apps
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView

from .forms import ModuleFormSet
from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Course, Module, Content


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
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        """Get form ModuleFormSet and fill in it with data"""
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """
        Send request to methods get or post.
        Get model Course with recent user.
        Save parameter "course" for other methods
        """
        self.course = get_object_or_404(Course, id=pk, author=request.user)
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


class ContentCreateAndUpdateView(TemplateResponseMixin, View):
    """Creation and updating content in different modules"""
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name):
        """Get class model if it name in ["text", "video", "image", "file"]"""
        if model_name in ("text", "video", "image", "file"):
            return apps.get_model(app_label="courses", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Form creation"""
        Form = modelform_factory(
            model,
            exclude=(
                "author",
                "order",
                "created_at",
                "updated_at",
            ),
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """Update and save class attributes: module, model, id"""
        self.module = get_object_or_404(
            Module,
            id=module_id,
            course__author=request.user,
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model,
                id=id,
                author=request.user,
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()

            if not id:
                Content.object.create(module=self.module, item=obj)
            return redirect("module_content_list", self.module.id)
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(View):
    """Delete content"""

    def post(self, request, id):
        content = get_object_or_404(
            Content,
            id=id,
            module__course__author=request.user,
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect("module_content_list", module.id)


class AllModuleContentListView(TemplateResponseMixin, View):
    """
    Display all modul of the course
    """

    def get(self, request, module_id):
        module = get_object_or_404(
            Module,
            id=module_id,
            course__author=request.user,
        )
        return self.render_to_response({"module": module})
