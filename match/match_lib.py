from __future__ import annotations
#https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
from enum import Enum
from decimal import Decimal, getcontext
from typing import Union, List, Tuple

from users.models import UserProfile

getcontext().prec = 2

MATCHING_POW = 2

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
    -  A multiple choice one with every next option is better that the
    previous one, e.g. "How good a you in C#"?
    (1-"never heard", 2-"a beginner", ... 5-"a C++ guru")
    """
    yes_no = 10
    gradation = 20


class UserType(Enum):
    candidate = UserProfile.CANDIDATE
    employer = UserProfile.EMPLOYER


class Answer:
    def __init__(self,
                 q_id: int,
                 u_type: UserType,
                 q_type: QuestionType,
                 value: DecimalInput,
                 weight: DecimalInput = 1):
        """
        Class to handle single answer data.
        To avoid float rounding errors value and weight are stored as decimals
        :param q_id: question id in Database
        :param q_type: question type
        :param value: answer value
        :param weight: answer weight
        :param u_type: user type
        """
        self.q_type = q_type
        self.q_id = q_id
        self.value = Decimal(value)
        self.weight = Decimal(weight)
        self.u_type = u_type

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
        if self.q_type != other.q_type:
            raise MatchError(f'{self} and {other} should have the same '
                             f'question type')
        # here distancing begins
        # note that self.weight is always used since self is the desired
        # answers of the person who looks through other answers to find the
        # best match so self.weight defines the importance of the answer
        if self.q_id == other.q_id:
            return (other.value - self.value) * self.weight
        else:
            return Decimal(0)

    def rank_answers(self, answers: List[Answer]) -> List[Tuple[Answer, Decimal]]:
        """
        method to get list of answers,
        :param answers:
        :return:
        """
        result = [(answer, self - answer) for answer in answers]
        return result.sort(key=lambda tup: tup[1])


# -----------------------------

_questions = [         
    { 'id': 0, 'type': Q_YN, 'value': 1, 'weight': 0.75 },
    { 'id': 1, 'type': Q_GT, 'value': 0.75, 'weight': 1.0 },
    { 'id': 2, 'type': Q_EQ, 'value': 0.5, 'weight': 0.5 }
]

_answers = { 0: 1, 1: 0.5, 2: 0.4 }

_skill_questions = [
    { 'id': 0, 'type': Q_GT, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.9 },
    { 'id': 1, 'type': Q_GT, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.9 }
]

_skill_answers = {
    0: { 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 },
    1: { 'skill_level': 0.6, 'wish_to_learn': 0.5, 'wish_to_engage': 1.0 }
}

# Matches a pair of one question and one answer
# Raises the "MatchError" custom exception if fails
def match_pair(q, a):
    if a < 0.0 or a > 1.0:  # If "a" value does not belong to [0, 1.0] range...
        raise MatchError
    if not 'weight' in q:   # If weight is not specified - make it "1.0"
        weight = 1.0
    else:
        weight = q['weight']

    # weight = q.get('weight', 1) is much simpler

    if q['type'] == Q_YN:                       # A "yes-no" question
        return (q['value'] - a) * weight
    if q['type'] == Q_GT:                       # A "greater than" one
        diff = q['value'] - a
        if not (diff > 0): # the < operation hasn't yet been invented, huh?
            return 0
        return diff * weight
    if q['type'] == Q_EQ:                       # An "equal to" one
        return (q['value'] - a) * weight
    raise MatchError


# Matches an array-like of questions with a dictionary of answers
# "id" of a question matches the "key" of an answer, e.g. q = {'id': 1, ...} => a = { 1: {}, ... }
# Raises the "MatchError" custom exception if fails
# Input: "questions" - array-like; "anwsers" - dictionary; 
# "method" - matching method (by now it is a number to power the matching error up to)
def match_questions(questions, answers, method=2):
    if method < 1:
        raise MatchError
    matching_errors_sum = 0.0
    must_have_errors_sum = 0.0
    for q in questions:
        if not (q['id'] in answers):    # If there is no answer for a question...
            a = 0.0                     # ... making it 0
        else:
            a = answers[ q['id'] ]
                  
        e = match_pair(q, a)
        matching_errors_sum += e**method
        if not q['weight'] < 1.0:
            must_have_errors_sum += e**method 

    error = matching_errors_sum**(1.0/method) if matching_errors_sum > 0.0 else 0.0
    must_have_error = must_have_errors_sum**(1.0/method) if must_have_errors_sum > 0.0 else 0.0

    return { 
        'error': error, 
        'must_have_error': must_have_error 
    } 
# end of match_questions                    

# Matches an array-like of questions with a dictionary of answers
# "id" of a question matches the "key" of an answer, e.g. q = {'id': 1, ...} => a = { 1: {}, ... }
# Raises the "MatchError" custom exception if fails
# Input: "questions" - array-like; "anwsers" - dictionary; 
# "method" - matching method (by now it is a number to power the matching error up to)
def match_skills(skill_questions, skill_answers, method=2):
    if method < 1:
        raise MatchError
    skill_errors_sum = 0.0
    overskill_errors_sum = 0.0
    wish_to_learn_errors_sum = 0.0
    wish_to_engage_errors_sum = 0.0;
    for sq in skill_questions:
        id = sq['id']
        # Calculating skill error
        q = { 'type': Q_GT, 'value': sq['skill_level'] }
        a = skill_answers[id]['skill_level'] if id in skill_answers else 0.0
        error = match_pair(q, a)
        skill_errors_sum += error**method
        
        q['type'] = Q_EQ    # Calculating overskill
        error = match_pair(q, a)
        if error < 0:
            overskill_errors_sum += error**method

        # Calculating "wish to learn" error
        q = { 'type': Q_GT, 'value': sq['wish_to_learn'] }
        a = skill_answers[id]['wish_to_learn'] if id in skill_answers else 0.0
        error = match_pair(q, a)
        wish_to_learn_errors_sum += error**method

        # Calculating "wish_to_engage" error
        q = { 'type': Q_GT, 'value': sq['wish_to_engage'] }
        a = skill_answers[id]['wish_to_engage'] if id in skill_answers else 0.0
        error = match_pair(q, a)
        wish_to_engage_errors_sum += error**method

        skill_error = skill_errors_sum**(1.0/method) if skill_errors_sum > 0.0 else 0.0 
        overskill_error = overskill_errors_sum**(1.0/method) if overskill_errors_sum > 0.0 else 0.0 
        wtl_error = wish_to_learn_errors_sum**(1.0/method) if wish_to_learn_errors_sum > 0.0 else 0.0 
        wte_error = wish_to_engage_errors_sum**(1.0/method) if wish_to_engage_errors_sum > 0.0 else 0.0 

    return { 
        'skill_error': skill_error, 
        'overskill_error': overskill_error,
        'wish_to_learn_error': wtl_error, 
        'wish_to_engage_error': wte_error
    }
#end of match_skills

print(match_questions(_questions, _answers), "\n")
print(match_skills(_skill_questions, _skill_answers), "\n")

_users_answers = [
    { 'u_id': 1, 'q_id': 0, 'value': 1.0 }, 
    { 'u_id': 1, 'q_id': 1, 'value': 0.5 }, 
    { 'u_id': 1, 'q_id': 2, 'value': 0.4 },  
    { 'u_id': 2, 'q_id': 0, 'value': 0.5 }, 
    { 'u_id': 2, 'q_id': 1, 'value': 0.75 }, 
    { 'u_id': 2, 'q_id': 2, 'value': 0.25 }   
]

def match_users( questions, answers ):
    users_scoreboard = dict()
    answers_indexed_by_user = dict()
    for i in range(len(answers)):
        u_id = answers[i]['u_id']
        if not (u_id in answers_indexed_by_user):
            answers_indexed_by_user[u_id] = list()
        answers_indexed_by_user[u_id].append(i)

    for user_id in answers_indexed_by_user:
        answers_to_match = dict()
        for index in answers_indexed_by_user[user_id]:
            answers_to_match[ answers[index]['q_id'] ] = answers[index]['value']
        users_scoreboard[user_id] = match_questions(questions, answers_to_match)            
    return users_scoreboard

print(match_users(_questions, _users_answers), "\n")

_users_skills = [
    { 'u_id': 1, 'q_id':0, 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 },
    { 'u_id': 1, 'q_id':1, 'skill_level': 0.6, 'wish_to_learn': 0.5, 'wish_to_engage': 1.0 },
    { 'u_id': 2, 'q_id':0, 'skill_level': 0.45, 'wish_to_learn': 0.75, 'wish_to_engage': 0.25 },
    { 'u_id': 2, 'q_id':1, 'skill_level': 0.6, 'wish_to_learn': 0.5, 'wish_to_engage': 1.0 }
]

# 0: { 'skill_level': 0.5, 'wish_to_learn': 0.9, 'wish_to_engage': 0.5 }
def match_users_by_skills( skill_questions, skill_answers ):
    users_scoreboard = dict()
    answers_indexed_by_user = dict()    # To have answers groupped by user
    for i in range(len(skill_answers)):
        u_id = skill_answers[i]['u_id']
        if not (u_id in answers_indexed_by_user):
            answers_indexed_by_user[u_id] = list()
        answers_indexed_by_user[u_id].append(i)

    for user_id in answers_indexed_by_user:
        answer_indexes = answers_indexed_by_user[user_id]
        user_answers = dict()
        for answer_index in answer_indexes:
            answer = skill_answers[ answer_index ]
            user_answers[ answer['q_id'] ] = answer
        users_scoreboard[user_id] = match_skills(skill_questions, user_answers)            
    
    return users_scoreboard

print(match_users_by_skills(_skill_questions, _users_skills), "\n")