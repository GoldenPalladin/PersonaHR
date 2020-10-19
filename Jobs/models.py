from django.db import models

from answers.models import Answers
from specializations.models import BaseModel, Specialization, SPECIALIZATION


class Job(BaseModel):
    """base class for position and cv"""
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+',
                                       verbose_name=SPECIALIZATION)
    answer_id = models.ForeignKey(Answers,
                                  on_delete=models.CASCADE,
                                  related_name='JobAnswers',
                                  name='answerId')
    answer_weight = models.IntegerField(name='answerWeight')
    min_salary = models.IntegerField(name='minSalary',
                                     blank=False)
    max_salary = models.IntegerField(name='maxSalary',
                                     blank=False)


class CV(Job):
    """
    class to store CV data
    """
    experience = models.TextField()


class Position(Job):
    """class to store Position description"""
    description = models.TextField()
