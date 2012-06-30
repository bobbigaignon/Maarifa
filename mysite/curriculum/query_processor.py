import re

from curriculum.models import Curriculum
from curriculum.models import Unit
from curriculum.models import Quizz
from curriculum.models import Question
from curriculum.models import QuizzQuestions
from curriculum.models import Choice
from curriculum.models import StudentQuizzHistory
from curriculum.models import Student


class QueryProcesser(object):
    flags = re.IGNORECASE
    get_matcher = re.compile('GET *(?P<curriculum>\w+) *(?P<level>\d+)$', flags=flags)
    take_matcher = re.compile('TAKE *(?P<curriculum>\w+) *(?P<level>\d+)$', flags=flags)
    submit_matcher = re.compile('SUBMIT *(?P<answers>.+)$', flags=flags)

    def _list_questions_for_quizz(self, quizz):
        # FIXME: Add order by
        return QuizzQuestions.objects.filter(quizz=quizz).all()

    def _list_choices_for_questions(self, question):
        # FIXME: Add order by
        return Choice.objects.filter(question=question).all()

    def _get_curriculum(self, curriculum_code, level):
        curriculum = Curriculum.objects.get(code=curriculum_code)
        unit = Unit.objects.get(curriculum=curriculum, level=level)
        return unit.body

    def _format_quizz(self, quizz):
        formatted_questions = []
        # FIXME: Add order by
        questions = self._list_questions_for_quizz(quizz)
        question_number = 1
        for question in questions:
            q = question.question
            formatted_question = ["{0}- {1}".format(question_number, q.body)]

            # Load possible choices
            formatted_choices = []
            choice_number = 1
            # FIXME: Add order by
            choices = self._list_choices_for_questions(q)
            for c in choices:
                formatted_choice = "{0}) {1}".format(
                    chr(65 + choice_number - 1),
                    c.body,
                    )
                formatted_choices.append(formatted_choice)
                choice_number = choice_number + 1

            formatted_question.extend(formatted_choices)
            formatted_questions.append(
                '\n'.join(formatted_question),
                )

            question_number = question_number + 1

        return '\n\n'.join(formatted_questions)

    def _get_quizz(self, curriculum_code, level, student):
        curriculum = Curriculum.objects.get(code=curriculum_code)
        unit = Unit.objects.get(curriculum=curriculum, level=level)

        # Check if the student has already take a quizz for the same unit
        if StudentQuizzHistory.objects.filter(unit=unit, student=student).all():
            raise Exception("Already took the quizz for that unit.")

        # Check if the student is currently taking a quizz
        if StudentQuizzHistory.objects.filter(student=student, answers=None).all():
            raise Exception("Already taking the quizz. Waiting for student to submit his answers.")

        # Get a random quizz for the given unit
        quizz = Quizz.objects.get(unit=unit)

        # Record that the student has taken a quizz for the given unit
        StudentQuizzHistory.objects.create(
            unit=unit,
            quizz=quizz,
            student=student,
            )

        return self._format_quizz(quizz)

    def process_user_request(self, phone_number, request_string):
        """Analyze a user string and response accordingly.

        User's query are expected to follow this format:
        [ACTION] <OBJECTS>

        The following actions are currently supported:

        * GET <curriculum name> <level>: gets a curriculum unit of the
          given level. Units are courses on various topics and come along
          with case studies that will help the student applying his
          knowledge to concrete examples.

        * TAKE <curriculum name> <level>: gets a quizz for a given
          curriculum unit. Quizzes are a series of multiple choice
          questions that will assess the user's knowledge of the unit.

        * SUBMIT <quizz hash tag> [<question number>: <answer>]: submits
          answers to a quizz that was sent to the user. the quizz is
          identified by a hash tag, which was sent alongside the quizz.

          Once properly parsed, the user's request will be analyzed and a
          response, in the form of a string, will be returned.

        """
        request_string = request_string.upper()
        student = self._get_student(phone_number)

        if self.get_matcher.match(request_string) is not None:
            matcher = self.get_matcher.match(request_string)
            return self._get_curriculum(
                matcher.group('curriculum'),
                matcher.group('level'),
                )

        elif self.take_matcher.match(request_string) is not None:
            matcher = self.take_matcher.match(request_string)
            return self._get_quizz(
                matcher.group('curriculum'),
                matcher.group('level'),
                student,
                )

        elif self.submit_matcher.match(request_string) is not None:
            matcher = self.submit_matcher.match(request_string)
            return self._parse_answers(matcher.group('answers'), student)

        return "DID NOT RECOGNIZE QUERY"

    def _parse_answers(self, answers, student):
        quizz_taken = StudentQuizzHistory.objects.filter(student=student, answers=None).all()
        if not quizz_taken:
            raise Exception("Not quizz currently taken")

        assert len(quizz_taken) == 1

        # Parse answers to a dictionary mapping question number to
        # submitted answer.
        parsed_answers = {}
        for answer in re.split(' +', answers):
            q, a = answer.split(':')
            parsed_answers[q] = a

        # Verify the answers submitted for each question
        correct_answers = 0

        quizz = quizz_taken[0].quizz
        questions = self._list_questions_for_quizz(quizz)
        index = 1
        for question in questions:
            q = question.question

            choices = list(self._list_choices_for_questions(q))
            correct_answer = Choice.objects.get(question=q, correct=True)
            correct_answer_index = choices.index(correct_answer)
            correst_answer_code = chr(65 + correct_answer_index)

            if parsed_answers[str(index)] == correst_answer_code:
                correct_answers = correct_answers + 1

            index = index + 1

        # Save answers
        quizz_taken.answers = answers
        quizz_taken.correct_answers = correct_answers

        return "You've got %d out of %d questions right." % (correct_answers, index - 1)

    def _get_student(self, phone_number):
        if not Student.objects.filter(phone_number=phone_number).all():
            return Student.objects.create(name="John Doe", phone_number=phone_number)

        return Student.objects.get(phone_number=phone_number)
