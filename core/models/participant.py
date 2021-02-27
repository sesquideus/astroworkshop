from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(AbstractUser):
    class Meta:
        ordering = ['last_name', 'first_name']

    affiliations = models.ManyToManyField(
        'Institute',
        through='Affiliation'
    )
    participations = models.ManyToManyField(
        'Event',
        through='Participation',
        related_name = 'participants'
    )
    about = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
