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
    path("<int:pk>/change/", CourseUpdateView.as_view(), name="change_course"),
    path("<int:pk>/delete/", CourseDeleteView.as_view(), name="delete_course"),
]
