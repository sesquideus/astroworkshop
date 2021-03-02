from django.db import models
from django.db.models import Prefetch, F, Q
from django.contrib.auth.models import AbstractUser, UserManager

from .slot import Slot


class ParticipantQuerySet(models.QuerySet):
    def with_talks(self):
        return self.prefetch_related(
            Prefetch(
                'slots',
                queryset=Slot.objects.filter(Q(category=Slot.CATEGORY_TALK) | Q(category=Slot.CATEGORY_WORKSHOP)),
                to_attr='talks',
            ),
        )



class Participant(AbstractUser):
    """
        Overrides the built-in Django User model and adds affiliations and workshop participations
    """
    class Meta:
        ordering = ['last_name', 'first_name']

    objects = UserManager.from_queryset(ParticipantQuerySet)()

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
