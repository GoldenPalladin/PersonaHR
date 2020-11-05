from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from .models import Skill, Response, SkillGroup


class SkillsInline(admin.TabularInline):
    model = Skill
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    }


class SkillGroups(admin.ModelAdmin):
    model = SkillGroup
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    }
    inlines = [
        SkillsInline,
    ]


class SkillResponses(admin.ModelAdmin):
    model = Response
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':120})},
    }


# admin.site.register(Skill, SkillsInline)
admin.site.register(SkillGroup, SkillGroups)
admin.site.register(Response, SkillResponses)
