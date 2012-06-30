import re

from curriculum.models import Curriculum
from curriculum.models import Unit
from curriculum.models import Quizz
from curriculum.models import Question
from curriculum.models import QuizzQuestions
from curriculum.models import Choice


class QueryProcesser(object):
    flags = re.IGNORECASE
    get_matcher = re.compile('GET *(?P<curriculum>\w+) *(?P<level>\d+)$', flags=flags)
    take_matcher = re.compile('TAKE *(?P<curriculum>\w+) *(?P<level>\d+)$', flags=flags)
    submit_matcher = re.compile('SUBMIT *(?P<quizz_hash>\w+) *(?P<answers>.+)$', flags=flags)

    def _get_curriculum(self, curriculum_code, level):
        curriculum = Curriculum.objects.get(code=curriculum_code)
        unit = Unit.objects.get(curriculum=curriculum, level=level)
        return unit.body

    def _format_quizz(self, quizz):
        formatted_questions = []
        questions = QuizzQuestions.objects.filter(quizz=quizz).all()
        question_number = 1
        for question in questions:
            q = question.question
            formatted_question = ["{0}- {1}".format(question_number, q.body)]

            # Load possible choices
            formatted_choices = []
            choice_number = 1
            choices = Choice.objects.filter(question=q).all()
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

    def _get_quizz(self, curriculum_code, level):
        curriculum = Curriculum.objects.get(code=curriculum_code)
        unit = Unit.objects.get(curriculum=curriculum, level=level)
        quizz = Quizz.objects.get(unit=unit)
        return self._format_quizz(quizz)

    def _process_user_request(self, request_string):
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
                )

        return "DID NOT RECOGNIZE QUERY"
