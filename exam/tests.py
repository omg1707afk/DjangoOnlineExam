from django.test import TestCase, Client
from django.urls import reverse
from .models import OnlineCourse, Lesson, Question, Choice, Submission


class ExamAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = OnlineCourse.objects.create(
            name="Python Basics",
            description="Introduction to Python programming."
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Variables and Types",
            content="Lesson content here.",
            order=1
        )
        self.question = Question.objects.create(
            lesson=self.lesson,
            text="What is 2 + 2?"
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="4",
            is_correct=True
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            text="5",
            is_correct=False
        )

    def test_models_str_methods(self):
        self.assertEqual(str(self.course), "Python Basics")
        self.assertEqual(str(self.lesson), "Variables and Types")
        self.assertEqual(str(self.question), "What is 2 + 2?")
        self.assertEqual(str(self.correct_choice), "4")

    def test_course_details_view(self):
        url = reverse("exam:course_details", kwargs={"course_id": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Basics")
        self.assertContains(response, "Variables and Types")

    def test_mock_exam_get_and_post(self):
        url = reverse("exam:mock_exam", kwargs={"lesson_id": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Mock Exam")

        # Submit answer
        post_response = self.client.post(url, {
            "student_name": "Alice",
            f"question_{self.question.id}": self.correct_choice.id
        })
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, "Congratulations, Alice!")
        self.assertContains(post_response, "Your Score: 1 / 1")

    def test_submit_and_show_result_views(self):
        submit_url = reverse("exam:submit", kwargs={"course_id": self.course.id})
        response = self.client.post(submit_url, {
            "student_name": "Bob",
            f"question_{self.question.id}": self.correct_choice.id
        })
        self.assertEqual(response.status_code, 302)

        # Follow redirect to show_exam_result
        result_response = self.client.get(response.url)
        self.assertEqual(result_response.status_code, 200)
        self.assertContains(result_response, "Congratulations, Bob!")
        self.assertContains(result_response, "1 / 1")
