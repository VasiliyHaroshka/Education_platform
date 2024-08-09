from django.contrib import admin

from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
    list_editable = ("title",)
    save_on_top = True
