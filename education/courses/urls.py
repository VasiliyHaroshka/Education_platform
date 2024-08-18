from django.urls import path

from .views import (
    CourseManageListView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
)

urlpatterns = [
    path("mine/", CourseManageListView.as_view(), name="manage_course_list"),
    path("create/", CourseCreateView.as_view(), name="create_course"),
    path("<pk:int>/change/", CourseUpdateView.as_view(), name="change_course"),
    path("<pk:int>/delete/", CourseDeleteView.as_view(), name="delete_course"),
]
