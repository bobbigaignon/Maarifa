from django.contrib import admin

from curriculum.models import Curriculum
from curriculum.models import Unit
from curriculum.models import Quizz
from curriculum.models import Question
from curriculum.models import Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


class QuizzAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Curriculum)
admin.site.register(Unit)
admin.site.register(Quizz, QuizzAdmin)
admin.site.register(Question, QuestionAdmin)
