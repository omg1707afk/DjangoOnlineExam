
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import OnlineCourse, Lesson, Question, Choice, Submission


class QuestionInline(TabularInline):
    model = Question
    extra = 1


class ChoiceInline(TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(ModelAdmin):
    list_display = ("text", "lesson")
    inlines = [ChoiceInline]


class LessonAdmin(ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    inlines = [QuestionInline]


admin.site.register(OnlineCourse)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
