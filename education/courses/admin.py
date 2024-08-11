from django.contrib import admin

from .models import Subject, Course, Module


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Register Subject model to admin panel"""
    list_display = ("title", "slug")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    save_on_top = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Register Course model to admin panel"""
    list_display = ("title", "description", "created_at")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    save_on_top = True
    inlines = (ModuleInline,)


admin.site.site_title = "Образовательная платформа"
admin.site.site_header = "Образовательная платформа"
