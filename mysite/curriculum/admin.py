from django.contrib import admin

from curriculum.models import Curriculum
from curriculum.models import Unit
from curriculum.models import Quizz
from curriculum.models import Question
from curriculum.models import Choice

admin.site.register(Curriculum)
admin.site.register(Unit)
admin.site.register(Quizz)
admin.site.register(Question)
admin.site.register(Choice)
