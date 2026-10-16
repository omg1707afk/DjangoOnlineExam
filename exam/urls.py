from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("exam/<int:lesson_id>/", views.mock_exam, name="mock_exam"),
]
