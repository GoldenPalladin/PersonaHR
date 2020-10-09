from django.contrib import admin

# Register your models here.

from .models import Specialization, Answers
admin.site.register(Specialization)
admin.site.register(Answers)

