from django.contrib import admin

# Register your models here.
from django.db import models
from django.forms import TextInput, Textarea

from answers.models import Response
from .models import Specialization, Respondent
admin.site.register(Specialization)
admin.site.register(Respondent)


class SkillResponses(admin.ModelAdmin):
    model = Response
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':120})},
    }


admin.site.register(Response, SkillResponses)
