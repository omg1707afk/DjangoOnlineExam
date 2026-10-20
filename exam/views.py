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
        selected_ids = []
        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            if choice_id:
                try:
                    selected_ids.append(int(choice_id))
                except (ValueError, TypeError):
                    pass

        score = 0
        for question in questions:
            if question.is_get_score(selected_ids):
                score += getattr(question, 'grade', 1) or 1

        result = {
            "student_name": student_name,
            "score": score,
            "total": len(questions),
        }

        submission = Submission.objects.create(
            student_name=student_name,
            score=score,
            total_questions=len(questions)
        )
        if selected_ids:
            submission.choices.set(selected_ids)

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

    selected_choice_ids = []
    for question in questions:
        choice_id = request.POST.get(f"question_{question.id}")
        if choice_id:
            try:
                selected_choice_ids.append(int(choice_id))
            except (ValueError, TypeError):
                pass

    score = 0
    for question in questions:
        if question.is_get_score(selected_choice_ids):
            score += getattr(question, 'grade', 1) or 1

    submission = Submission.objects.create(
        student_name=student_name,
        score=score,
        total_questions=questions.count()
    )
    if selected_choice_ids:
        submission.choices.set(selected_choice_ids)

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

    questions = Question.objects.filter(lesson__course=course)
    selected_ids = list(submission.choices.values_list("id", flat=True))

    total_score = 0
    possible_score = 0

    for question in questions:
        q_grade = getattr(question, "grade", 1) or 1
        possible_score += q_grade
        if question.is_get_score(selected_ids):
            total_score += q_grade

    if total_score == 0 and submission.score > 0:
        total_score = submission.score
    if possible_score == 0 and submission.total_questions > 0:
        possible_score = submission.total_questions

    context = {
        "course": course,
        "submission": submission,
        "selected_ids": selected_ids,
        "grade": total_score,
        "possible": possible_score,
        "total_score": total_score,
        "possible_score": possible_score,
    }

    return render(request, "exam/exam_result_bootstrap.html", context)
