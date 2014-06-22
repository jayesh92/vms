from django.contrib import admin
from AdminUnit.models import UserProfile, Event, AssignedJob
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(AssignedJob)
