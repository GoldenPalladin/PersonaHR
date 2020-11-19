from django.db import models
from users.models import UserProfile

from specializations.models import BaseModel, Specialization, SPECIALIZATION


class Job(BaseModel):
    """base class for position and cv"""
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+',
                                       verbose_name=SPECIALIZATION)
    min_salary = models.IntegerField(name='minSalary',
                                     blank=False)
    max_salary = models.IntegerField(name='maxSalary',
                                     blank=False)
    user_profile = models.ForeignKey(UserProfile,
                                     name='userProfile',
                                     on_delete=models.SET_NULL,
                                     related_name='user_profile',
                                     null=True,
                                     blank=True)


class CV(Job):
    """
    class to store CV data
    """
    experience = models.TextField(blank=True)


class Position(Job):
    """class to store Position description"""
    description = models.TextField(blank=True)
