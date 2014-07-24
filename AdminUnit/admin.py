from django.contrib import admin
from AdminUnit.models import UserProfile, Event, Job, Organization, Shift
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Job)
admin.site.register(Organization)
admin.site.register(Shift)
