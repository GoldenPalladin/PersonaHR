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
LEAD_SOURCE = 'Respondent source url'
DEFAULT_LEAD_SOURCE = 'http://localhost'


class Specialization(models.Model):
    """ class to handle specialization tags"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Questions(models.Model):
    """class to store questions (grouping item for options)"""
    RADIO = 'SingleChoice'
    CHECK = 'MultipleChoice'
    NUMBER = 'Number'
    TEXT = 'FreeText'
    QUESTION_TYPE_CHOICE = [(RADIO, 'Single choice'),
                            (CHECK, 'Multiple choice'),
                            (NUMBER, 'Number'),
                            (TEXT, 'Text')]
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+')

    question_type = models.CharField(max_length=15,
                                     name='questionType',
                                     choices=QUESTION_TYPE_CHOICE,
                                     default=RADIO,
                                     verbose_name=QUESTION_TYPE)

    em_text = models.TextField(name='textForEmployer',
                               verbose_name=EM_TEXT_NAME,
                               default='')

    ca_text = models.TextField(name='textForCandidate',
                               verbose_name=CA_TEXT_NAME,
                               default='')

    weight = models.IntegerField()

    def __str__(self):
        return f'Question {self.id}: {self.textForEmployer}'


class QuestionOptions(models.Model):
    """class to store question options (radio/checkbox options)"""
    question = models.ForeignKey(Questions,
                                 on_delete=models.CASCADE,
                                 related_name='options',
                                 verbose_name=QUESTION_GROUP)

    order_no = models.SmallIntegerField(default=1, verbose_name=ORDER_NO)

    em_text = models.TextField(name='textForEmployer',
                               verbose_name=EM_TEXT_NAME,
                               default='')

    ca_text = models.TextField(name='textForCandidate',
                               verbose_name=CA_TEXT_NAME,
                               default='')

    weight = models.IntegerField()

    def __str__(self):
        return f'{self.order_no}: {self.em_text} - {self.ca_text} ({self.weight})'


class UserProfile(models.Model):
    """
    Class to handle additional user data not matching to User model
    """
    CANDIDATE = 'candidate'
    EMPLOYER = 'employer'
    USER_TYPE_CHOICE = [(CANDIDATE, 'Candidate'),
                        (EMPLOYER, 'Employer')]

    lead_source = models.URLField(name='leadSource',
                                  verbose_name=LEAD_SOURCE,
                                  default=DEFAULT_LEAD_SOURCE)

    user_type = models.CharField(max_length=9,
                                 name='userType',
                                 choices=USER_TYPE_CHOICE,
                                 default=CANDIDATE)
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


class Answers(models.Model):
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

    answer_data = models.JSONField(name='answers')

    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='+')

    added = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.added} - User: {self.user.username}, ' \
            f'type: {self.user_type}'


