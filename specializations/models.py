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
    specialization = models.ForeignKey(Specialization,
                                       on_delete=models.CASCADE,
                                       related_name='specialization',
                                       verbose_name=SPECIALIZATION)

    em_text = models.TextField(name='textForEmployer',
                               verbose_name=EM_TEXT_NAME,
                               default='')

    ca_text = models.TextField(name='textForCandidate',
                               verbose_name=CA_TEXT_NAME,
                               default='')

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

    def __str__(self):
        return f'{self.order_no}: {self.textForEmployer} - {self.textForCandidate} ({self.weight})'


SKILL_NAME = 'Skill'
SKILL_GROUP = 'Group'


class SkillGroup(BaseModel):
    name = models.CharField(max_length=100,
                            name='skillGroup',
                            verbose_name=SKILL_GROUP)
    def __str__(self):
        return f'{self.skillGroup}'


class Skill(BaseModel):
    group = models.ForeignKey(SkillGroup,
                              on_delete=models.CASCADE,
                              related_name='group',
                              verbose_name=SKILL_GROUP)
    name = models.CharField(max_length=100,
                            name='skillName',
                            verbose_name=SKILL_NAME)

    def __str__(self):
        return f'{self.skillName}'