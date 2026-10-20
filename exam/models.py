from django.db import models


class OnlineCourse(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


# Alias Course for compatibility
Course = OnlineCourse


class Instructor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Learner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        OnlineCourse,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.TextField()
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.text[:80]

    def is_get_score(self, selected_ids):
        all_answers = self.choices.filter(is_correct=True).count()
        selected_correct = self.choices.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers > 0 and all_answers == selected_correct:
            return True
        return False


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(models.Model):
    student_name = models.CharField(max_length=100)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    choices = models.ManyToManyField(Choice, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.score}/{self.total_questions}"