from django.db import models
from django.contrib.auth import get_user_model

from specializations.models import BaseModel

User = get_user_model()

T_USER_ID = 'Telegram user ID'
T_USER_F_NAME = 'Telegram user first name'
T_USER_L_NAME = 'Telegram user last name'
T_USER_U_NAME = 'Telegram user nickname'
LEAD_SOURCE = 'Respondent source url'
DEFAULT_LEAD_SOURCE = 'http://localhost'


class UserProfile(BaseModel):
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
