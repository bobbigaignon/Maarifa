from django.contrib import admin

from curriculum.models import Curriculum
from curriculum.models import Unit
from curriculum.models import Quizz
from curriculum.models import Question
from curriculum.models import Choice
from curriculum.models import QuizzQuestions
from curriculum.models import Student
from curriculum.models import StudentQuizzHistory


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Curriculum)
admin.site.register(Unit)
admin.site.register(Quizz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizzQuestions)
admin.site.register(StudentQuizzHistory)
admin.site.register(Student)
