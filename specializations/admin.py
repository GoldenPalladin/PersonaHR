from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
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
