from django.db import models
from django.core.validators import RegexValidator

class Volunteer(models.Model):
    first_name = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    last_name = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    address = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)]+$',
            ),
        ],
    )
    city = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    state = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    country = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
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
    company = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    #EmailField automatically checks if email address is a valid format 
    email = models.EmailField(max_length=20)
    websites = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\.)]+$',
            ),
        ],
    )
    description = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(\.)]+$',
            ),
        ],
    )
    resume = models.TextField(blank=True)
    #do validation
    resume_file = models.FileField(upload_to='resumes/', max_length=40, blank=True)
