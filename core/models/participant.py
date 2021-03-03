from django.db import models
from django.db.models import Prefetch, F, Q
from django.contrib.auth.models import AbstractUser, UserManager

from .slot import Slot
from .affiliation import Affiliation
from .institute import Institute


class ParticipantQuerySet(models.QuerySet):
    def with_talks(self):
        return self.prefetch_related(
            Prefetch(
                'slots',
                queryset=Slot.objects.filter(Q(category=Slot.CATEGORY_TALK) | Q(category=Slot.CATEGORY_WORKSHOP)),
                to_attr='talks',
            ),
        )

    def with_current_affiliations(self, date):
        return self.prefetch_related(
            Prefetch(
                'affiliations',
                queryset=Institute.objects.exclude(Q(affiliation__start__gte=date) | Q(affiliation__end__lte=date)).distinct(),
                to_attr='current_affiliations',
            ),
        )

    def for_event(self, event_code):
        return self.filter(participations__code=event_code)


class Participant(AbstractUser):
    """
        Overrides the built-in Django User model and adds affiliations and workshop participations
    """
    class Meta:
        ordering = ['last_name', 'first_name']

    objects = UserManager.from_queryset(ParticipantQuerySet)()

    affiliations = models.ManyToManyField(
        'Institute',
        through='Affiliation',
        related_name = 'people',
    )
    participations = models.ManyToManyField(
        'Event',
        through='Participation',
        related_name = 'participants',
    )
    about = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
