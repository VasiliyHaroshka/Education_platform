from .models import Course


class OwnerMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ("title", "")
