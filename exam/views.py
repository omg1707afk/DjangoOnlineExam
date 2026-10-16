from django.shortcuts import get_object_or_404, render
from .models import OnlineCourse, Lesson, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(
        OnlineCourse.objects.prefetch_related("lessons"),
        pk=course_id
    )
    return render(
        request,
        "exam/course_details_bootstrap.html",
        {"course": course}
    )


def mock_exam(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.prefetch_related("questions__choices"),
        pk=lesson_id
    )
    questions = list(lesson.questions.all())
    result = None

    if request.method == "POST":
        student_name = request.POST.get("student_name", "").strip() or "Student"
        score = 0

        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            if choice_id and Choice.objects.filter(
                id=choice_id,
                question=question,
                is_correct=True
            ).exists():
                score += 1

        result = {
            "student_name": student_name,
            "score": score,
            "total": len(questions),
        }

        Submission.objects.create(
            student_name=student_name,
            score=score,
            total_questions=len(questions)
        )

    return render(request, "exam/mock_exam.html", {
        "lesson": lesson,
        "questions": questions,
        "result": result,
    })
