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


class QuestionInline(admin.StackedInline):
    model = QuizzQuestions
    extra = 0


class QuizzAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'number_of_questions']
    inlines = [QuestionInline]


class StudentQuizzHistoryAdmin(admin.ModelAdmin):
    list_display = ['student', 'quizz', 'unit', 'correct_answers']


admin.site.register(Curriculum)
admin.site.register(Unit)
admin.site.register(Quizz, QuizzAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(StudentQuizzHistory, StudentQuizzHistoryAdmin)
admin.site.register(Student)
