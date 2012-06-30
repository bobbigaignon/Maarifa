from django.db import models


class Curriculum(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=15, unique=True)

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
    body = models.TextField()

    def __unicode__(self):
        return self.body


class QuizzQuestions(models.Model):
    """Auxiliary table that links a quizz to a set of questions"""
    quizz = models.ForeignKey(Quizz)
    question = models.ForeignKey(Question)

    class Meta:
        unique_together = ('question', 'quizz')


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


class Student(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)


class StudentQuizzHistory(models.Model):
    """Records history of test taken by students."""
    unit = models.ForeignKey(Unit)
    quizz = models.ForeignKey(Quizz)
    student = models.ForeignKey(Student)
    answers = models.TextField(null=True)
    correct_answers = models.IntegerField(null=True)

    class Meta:
        unique_together = ('student', 'quizz')
