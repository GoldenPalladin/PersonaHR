from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from specializations.models import Skill, SkillGroup
from .models import Questions, QuestionOptions


class QuestionOptionsInline(admin.TabularInline):
    model = QuestionOptions
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':80})},
    }


class QuestionsAdmin(admin.ModelAdmin):
    model = Questions
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':120})},
    }
    inlines = [
        QuestionOptionsInline,
    ]


admin.site.register(Questions, QuestionsAdmin)


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


admin.site.register(SkillGroup, SkillGroups)
