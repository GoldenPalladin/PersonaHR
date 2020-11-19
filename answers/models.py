from django.db import models

from specializations.models import BaseModel, Specialization, \
    SPECIALIZATION, QuestionOptions, Skill, SKILL_NAME
from users.models import UserProfile, User
from Jobs.models import CV, Job


class Respondent(BaseModel):
    """
    Class to store response data both from candidates and employers
    """

    cv = models.ForeignKey(CV,
                           on_delete=models.CASCADE,
                           blank=True)

    # answer_data = models.TextField(name='answerData',
    #                                null=True,
    #                                blank=True)

    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.added} - User: {self.user.username}'


class Selected(BaseModel):
    """
    base class to store items selected by respondent
    """
    respondent = models.ForeignKey(Respondent,
                                   on_delete=models.CASCADE,
                                   related_name='respondent',
                                   name='respondentId')

    selection_weight = models.IntegerField(name='selectionWeight')


class SelectedOptions(Selected):
    """
    class to handle selected options
    """
    selected_option_id = models.ForeignKey(QuestionOptions,
                                           on_delete=models.SET_NULL,
                                           name='selectedOptionId',
                                           null=True)


SKILL_LEVEL = 'What is your level in this skill?'
SKILL_LEVEL_CHOICES = [(1, 'Do not have this skill'),
                       (2, 'Actively learning'),
                       (3, 'Using from time to time'),
                       (4, 'Using every day'),
                       (5, 'Expert')]


class Response(Selected):
    """
    class to handle answered skill-level
    """
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='skill',
                              verbose_name=SKILL_NAME)

    skill_level = models.IntegerField(name='skillLevel',
                                      choices=SKILL_LEVEL_CHOICES,
                                      default=1,
                                      verbose_name=SKILL_LEVEL)