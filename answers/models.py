from django.db import models
from taggit.managers import TaggableManager

from specializations.models import BaseModel, Specialization, \
    SPECIALIZATION, QuestionOptions
from users.models import UserProfile, User


class Answers(BaseModel):
    """
    Class to store response data both from candidates and employers
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='+',
                             null=True,
                             blank=True)

    user_profile = models.ForeignKey(UserProfile,
                                     name='userProfile',
                                     on_delete=models.SET_NULL,
                                     related_name='user_profile',
                                     null=True,
                                     blank=True)

    answer_data = models.JSONField(name='answerData')

    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+',
                                       verbose_name=SPECIALIZATION)

    added = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.added} - User: {self.user.username}, ' \
            f'type: {self.user_type}'


class ParsedAnswers(models.Model):
    """
    class to store answers after
    """
    answer_id = models.ForeignKey(Answers,
                                  on_delete=models.CASCADE,
                                  related_name='answers',
                                  name='answerId')
    selected_option_id = models.ForeignKey(QuestionOptions,
                                           on_delete=models.SET_NULL,
                                           name='selectedOptionId',
                                           null=True)
    answered_option_weight = models.IntegerField(name='answeredOptionWeight')



