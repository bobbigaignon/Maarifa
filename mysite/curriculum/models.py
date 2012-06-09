from django.db import models


class Curriculum(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class Unit(models.Model):
    curriculum = models.ForeignKey(Curriculum)
    level = models.IntegerField()
    body = models.TextField()

    def __unicode__(self):
        return unicode(self.curriculum) + ' (level %d)' % self.level

    class Meta:
        unique_together = ('curriculum', 'level')


class Quizz(models.Model):
    unit = models.ForeignKey(Unit)
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title


class Question(models.Model):
    quizz = models.ForeignKey(Quizz)
    body = models.TextField()

    def __unicode__(self):
        return '[%s]' % self.quizz + ' ' + self.body


class Choice(models.Model):
    # TODO: force exactly one correct answer per question.
    question = models.ForeignKey(Question)
    body = models.TextField()
    correct = models.BooleanField()

    def __unicode__(self):
        choice_str = self.body

        if self.correct:
            choice_str += ' (correct)'
        else:
            choice_str += ' (incorrect)'

        return choice_str
