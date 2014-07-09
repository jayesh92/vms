from django.core.validators import RegexValidator
from django.db import models

class Organization(models.Model):
    organization_name = models.CharField(
        unique=True,            
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)|(-)|(:)]+$',
            ),
        ],
    )
