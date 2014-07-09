from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    #links UserProfile to a User model instance
    user = models.OneToOneField(User)

    #additional attributes we wish to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    #override the unicode method to return out something meaningful
    def __unicode__(self):
        return self.user.username
