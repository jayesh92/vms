from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from organization.models import Organization

class Volunteer(models.Model):
    first_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    last_name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    address = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)]+$',
            ),
        ],
    )
    city = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    state = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    country = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\-)]+$',
            ),
        ],
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[0-9]+$',
            ),
        ],
    )
    unlisted_organization = models.CharField(
        blank=True,
        max_length=100,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\-)|(:)]+$',
            ),
        ],
    )
    #Organization to Volunteer is a one-to-many relationship
    organization = models.ForeignKey(Organization, null=True)
    #EmailField automatically checks if email address is a valid format 
    email = models.EmailField(max_length=45)
    websites = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\.)|(\-)|(?)|(=)|(#)|(:)|(/)|(_)|(&)]+$',
            ),
        ],
    )
    description = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$',
            ),
        ],
    )
    resume = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$',
            ),
        ],
    )
    #all resumes are stored in /srv/vms/resume/
    resume_file = models.FileField(upload_to='vms/resume/', max_length=75, blank=True)
    user = models.OneToOneField(User)
