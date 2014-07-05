from django.core.validators import RegexValidator
from django.db import models

class Job(models.Model):
    job_title = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(\s)]+$',
            ),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(
        blank=True,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$',
            ),
        ],
    )
