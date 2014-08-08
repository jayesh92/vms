from django.contrib import admin
from AdminUnit.models import *
from django.contrib.auth.models import User

admin.site.register(AdminProfile)
admin.site.register(VolunteerProfile)
admin.site.register(Event)
admin.site.register(Job)
admin.site.register(Organization)
admin.site.register(Shift)
