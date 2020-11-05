from django.db import models
from specializations.models import BaseModel
from Jobs.models import CV, Position

SKILL_NAME = 'Skill'
SKILL_GROUP = 'Group'
CV_NAME = 'Link to candidate CV'
POSITION_NAME = 'Link to position'
SKILL_LEVEL = 'What is your level in this skill?'
SKILL_LEVEL_CHOICES = [(1, 'Do not have this skill'),
                       (2, 'Actively learning'),
                       (3, 'Using from time to time'),
                       (4, 'Using every day'),
                       (5, 'Expert')]
SKILL_APPLICATION = 'Would you like to use this skill in your job?'
SKILL_GROWTH = 'Would you like to learn more on this skill?'
SKILL_APPLICATION_GROWTH_CHOICES = [(1, 'Do not want'),
                                    (2, 'I don\'t care'),
                                    (3, 'I\'d like to')]


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


class Response(BaseModel):
    """
    class to handle skill-position and skill-CV mappings
    """
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='skill',
                              verbose_name=SKILL_NAME)
    cv = models.ForeignKey(CV,
                           blank=True,
                           null=True,
                           on_delete=models.CASCADE,
                           verbose_name=CV_NAME)
    position = models.ForeignKey(Position,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 verbose_name=POSITION_NAME)
    skill_level = models.IntegerField(name='skillLevel',
                                      choices=SKILL_LEVEL_CHOICES,
                                      default=1,
                                      verbose_name=SKILL_LEVEL)
    skill_application = models.IntegerField(name='skillApplication',
                                            choices=SKILL_APPLICATION_GROWTH_CHOICES,
                                            default=2,
                                            verbose_name=SKILL_APPLICATION)
    skill_growth = models.IntegerField(name='skillGrowth',
                                       choices=SKILL_APPLICATION_GROWTH_CHOICES,
                                       default=2,
                                       verbose_name=SKILL_GROWTH)
    