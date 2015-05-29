from django.core.validators import RegexValidator
from django.db import models

class Event(models.Model):
    name = models.CharField(
        max_length=75,
        validators=[
            RegexValidator(
                r'^[(A-Z)|(a-z)|(0-9)|(\s)|(\.)|(,)|(\-)|(!)]+$',
            ),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField()
