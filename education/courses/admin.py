from django.contrib import admin

from .models import Subject, Course


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Register Subject model to admin panel"""
    list_display = ("title", "slug")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    list_editable = ("title",)
    save_on_top = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Register Course model to admin panel"""
    list_display = ("title", "description", "created_at")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    list_editable = ("title",)
    save_on_top = True
