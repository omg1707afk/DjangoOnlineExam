from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path("", views.course_details, {"course_id": 2}, name="index"),
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("courses/<int:course_id>/submit/", views.submit, name="submit"),
    path(
        "courses/<int:course_id>/submission/<int:submission_id>/result/",
        views.show_exam_result,
        name="show_exam_result",
    ),
    path("exam/<int:lesson_id>/", views.mock_exam, name="mock_exam"),
]
