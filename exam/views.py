
from django.shortcuts import get_object_or_404, render, redirect
from .models import OnlineCourse, Lesson, Question, Choice, Submission

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
        student_name = (
            request.POST.get("student_name", "").strip() or "Student"
        )
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


def submit(request, course_id):
    course = get_object_or_404(OnlineCourse, pk=course_id)

    if request.method != "POST":
        return redirect("exam:course_details", course_id=course.id)

    questions = Question.objects.filter(lesson__course=course)
    student_name = (
        request.POST.get("student_name", "").strip() or "Student"
    )
    score = 0

    for question in questions:
        choice_id = request.POST.get(f"question_{question.id}")
        if choice_id and Choice.objects.filter(
            pk=choice_id,
            question=question,
            is_correct=True
        ).exists():
            score += 1

    submission = Submission.objects.create(
        student_name=student_name,
        score=score,
        total_questions=questions.count()
    )

    return redirect(
        "exam:show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(OnlineCourse, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    return render(request, "exam/exam_result.html", {
        "course": course,
        "submission": submission,
    })

    
