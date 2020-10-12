from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()

QUESTION_GROUP = 'Question group name'
QUESTION_TYPE = 'Type of question group'
EM_TEXT_NAME = 'Text for employer'
CA_TEXT_NAME = 'Text for candidate'
ORDER_NO = 'Option position'
T_USER_ID = 'Telegram user ID'
T_USER_F_NAME = 'Telegram user first name'
T_USER_L_NAME = 'Telegram user last name'
T_USER_U_NAME = 'Telegram user nickname'


class Specialization(models.Model):
    """ class to handle specialization tags"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Questions(models.Model):
    """class to store questions (grouping item for options)"""
    RADIO = 'Rb'
    CHECK = 'Cb'
    NUMBER = 'Nm'
    TEXT = 'Tx'
    QUESTION_TYPE_CHOICE = [(RADIO, 'Single choice'),
                            (CHECK, 'Multiple choice'),
                            (NUMBER, 'Number'),
                            (TEXT, 'Text')]
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+')
    question_type = models.CharField(max_length=2,
                                     choices=QUESTION_TYPE_CHOICE,
                                     default=RADIO,
                                     verbose_name=QUESTION_TYPE)
    em_text = models.CharField(max_length=500, verbose_name=EM_TEXT_NAME)
    ca_text = models.CharField(max_length=500, verbose_name=CA_TEXT_NAME)
    weight = models.IntegerField()

    def __str__(self):
        return self.em_text


class QuestionOptions(models.Model):
    """class to store question options (radio/checkbox options)"""
    question = models.ForeignKey(Questions,
                                 on_delete=models.CASCADE,
                                 related_name='options',
                                 verbose_name=QUESTION_GROUP)
    order_no = models.SmallIntegerField(default=1, verbose_name=ORDER_NO)
    em_text = models.CharField(max_length=500, verbose_name=EM_TEXT_NAME)
    ca_text = models.CharField(max_length=500, verbose_name=CA_TEXT_NAME)
    weight = models.IntegerField()

    def __str__(self):
        return f'{self.order_no}: {self.em_text} - {self.ca_text} ({self.weight})'


class Answers(models.Model):
    """
    Class to store response data both from candidates and employers
    """
    CANDIDATE = 'Ca'
    EMPLOYER = 'Em'
    USER_TYPE_CHOICE = [(CANDIDATE, 'Candidate'),
                        (EMPLOYER, 'Employer')]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='+', null=True, blank=True)
    user_type = models.CharField(max_length=2,
                                 choices=USER_TYPE_CHOICE,
                                 default=CANDIDATE)
    answer_data = models.JSONField(name='answers')
    # Telegram bot user data
    b_user = models.CharField(max_length=20,
                              name='userID',
                              verbose_name=T_USER_ID, blank=True)
    b_user_f_name = models.CharField(max_length=20, blank=True,
                                     name='userFirstName',
                                     verbose_name=T_USER_F_NAME)
    b_user_l_name = models.CharField(max_length=20, blank=True,
                                     name='userLastName',
                                     verbose_name=T_USER_L_NAME)
    b_user_u_name = models.CharField(max_length=20, blank=True,
                                     name='userUserName',
                                     verbose_name=T_USER_U_NAME)
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+')
    added = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.added} - User: {self.user.username}, ' \
            f'type: {self.user_type}'


