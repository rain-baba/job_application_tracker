from django.contrib import admin

from .models import Application, Company, InterviewRound

admin.site.register(Company)
admin.site.register(Application)
admin.site.register(InterviewRound)
