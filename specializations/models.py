from django.db import models

QUESTION_GROUP = 'Question group name'
QUESTION_TYPE = 'Type of question group'
EM_TEXT_NAME = 'Text for employer'
CA_TEXT_NAME = 'Text for candidate'
ORDER_NO = 'Option position'
SPECIALIZATION = 'Job specialization'


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Specialization(BaseModel):
    """ class to handle specialization tags"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Questions(BaseModel):
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
                                       related_name='+',
                                       verbose_name=SPECIALIZATION)

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

    weight = models.IntegerField(default=1)

    def __str__(self):
        return f'Question {self.id}: {self.textForEmployer} - {self.textForCandidate}'


class QuestionOptions(BaseModel):
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

    weight = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.order_no}: {self.textForEmployer} - {self.textForCandidate} ({self.weight})'