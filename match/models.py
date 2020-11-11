
from django.db import models

class Match(models.Model):

    def __init__(self, **kwargs):
        for field in ('pk', 'name' ):
            setattr(self, field, kwargs.get(field, None))

    class Meta:
        ordering = ['pk']