from __future__ import annotations
#https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from enum import Enum
from dataclasses import dataclass, InitVar
from decimal import Decimal, getcontext
from typing import Union, List, Tuple

from users.models import UserProfile
from specializations.models import Questions

getcontext().prec = 2

DISTANCE_THRESHOLD = 100

"""
Concepts:
0. There is "I" who search for the best match among the "others" answer 
set. Answers 
1. Match is a distance. The closer the match, the less the distance. Ideal 
match makes zero distance
2. Distance is measured from "my answer" to "other's answer" with weight 
taken as importance parameter. The more the weight the less the distance
3. Question of single choice makes one "selected option" answer with weight, 
value. Distance is measured between "my" and "other" selected options.
Values of choices makes the [0...1] grade.
4. Question of multiple choice makes multiple "selected option" answers, 
each having weight and  possible values of [0, 1]. Distance is measured 
for each selected option.
5. Total distance -- sum of distances makes the total distance
6. Distance threshold -- for every question and skill distance is 
calculated and added. If at the N-th answer the distance threshold for 
"other's" exceeded, the "other" is excluded from the answer set.
Threshold value is a question of model norming.
"""

DecimalInput = Union[float, int, str]
# type that can be converted into Decimal


class MatchError(Exception):
    """
    A custom error to raise through matching if required
    """
    pass


# using classes is more convenient.
# And docstring is obligatory
class QuestionType(Enum):
    """
    Available question types:
    - A yes-no question of boolean type
    -  A single choice one with every next option is better that the
    previous one, e.g. "How good a you in C#"?
    (1-"never heard", 2-"a beginner", ... 5-"a C++ guru")
    """
    yes_no = Questions.CHECK
    gradation = Questions.RADIO


class UserType(Enum):
    candidate = UserProfile.CANDIDATE
    employer = UserProfile.EMPLOYER


@dataclass
class QuestionOption:
    """
    class to handle question options
    :param o_id: question option id
    :param value: option value
    :param weight: option answer weight
    """
    o_id: int
    value: DecimalInput
    weight: int

    def __post_init__(self):
        self.value = Decimal(self.value)

    def __sub__(self, other) -> Decimal:
        """
        redefine substraction as distance metric between answered options
        :param other:
        :return:
        """
        if not isinstance(other, QuestionOption):
            raise TypeError(f'{other} must be of {type(self)} type')
        # note that self.weight is always used since self is the desired
        # answers of the person who looks through other answers to find the
        # best match so self.weight defines the importance of the answer
        return Decimal(abs((other.value - self.value) * self.weight))

    def distance_to_options(self, options: List[QuestionOption]) -> Decimal:
        """
        Measure the distance between "my" option and list of answered
        "their" options. Used for multiple choice list of options selected
        :param options: list of "their" checked options
        :return: 0 if self is in options list, otherwise 1 * self.weight
        """
        if self.o_id in [option.o_id for option in options]:
            return Decimal(0)
        return Decimal(self.weight)


@dataclass
class Answer:
    """
    Class to handle answer data for one Question (single or multiple choice).
    To avoid float rounding errors value and weight are stored as decimals
    :param q_id: question id in Database
    :param q_type: question type
    :param u_type: user type
    :param selected_options: list of selected question options
    """
    q_id: int
    u_type: UserType
    q_type: QuestionType
    weight: int
    selected_options: List[QuestionOption]

# TODO: weight for SingleChoice, weights for MultipleChoice options

    def __sub__(self, other) -> Decimal:
        """
        redefine substraction as distance metric between answers
        :param other: answer of the other user type
        :return: decimal distance
        """
        if not isinstance(other, Answer):
            raise TypeError(f'{other} must be of {type(self)} type')
        if other.u_type == self.u_type:
            raise MatchError(f'{self} and {other} should have different '
                             f'user types, now they all are {self.u_type}')
        if self.q_id != other.q_id:
            raise MatchError(f'{self} and {other} should be the answers for '
                             f'the  same question')

        if self.q_type == QuestionType.gradation:
            return self.selected_options[0] - other.selected_options[0]
        elif self.q_type == QuestionType.yes_no:
            sum([option.distance_to_options(other.selected_options) for
                 option in self.selected_options])

    def distance_to_answers(self, others: Answers) -> Decimal:
        """
        Measure distance between "my" answer and list of "their's" answers.
        :param others: list of answers
        :return: if question with the same id is answered in 'others',
        the distance between "my" and "other" answer is returned, otherwise 0
        """
        same_question_answer = [answer for answer in others if self.q_id ==
                                answer.q_id]
        if same_question_answer:
            return self - same_question_answer[0]
        return Decimal(0)


class Answers(list):
    """
    class to represent list of answers
    """

    def __sub__(self, other) -> Decimal:
        """
        Distance between lists of answers is sum of distances between
        answers in each list
        :param other:
        :return:
        """
        if not isinstance(other, Answers):
            raise TypeError(f'{other} must be of {type(self)} type')
        return sum([answer.distance_to_answers(other) for answer in self])


@dataclass
class Respondent:
    """
    class to represent some user with list of questions and matching rank
    """
    answers: Answers
    distance: Decimal = DISTANCE_THRESHOLD
    uid: int = 0


@dataclass
class Questionaire:
    """
    Class to represent structure with "my" answers and list of respondents
    """
    my_answers: Answers
    respondents: List[Respondent]

    def rank_users(self):
        """
        Calculate distance for each respondent, pop out those beyond
        DISTANCE_THRESHOLD and sort the remaining by distance asc
        :return:
        """
        def respondent_key(r: Respondent) -> Decimal:
            return r.distance

        result = list()
        for respondent in self.respondents:
            distance = self.my_answers - respondent.answers
            if distance < DISTANCE_THRESHOLD:
                respondent.distance = distance
                result.append(respondent)
        self.respondents = sorted(result, key=respondent_key)
