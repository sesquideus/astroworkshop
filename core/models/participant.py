from django.db import models
from django.db.models import Prefetch, F, Q, Value
from django.db.models.functions import Concat
from django.contrib.auth.models import AbstractUser, UserManager

from .slot import Slot
from .event import Event
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

    def with_events(self):
        return self.prefetch_related(
            Prefetch(
                'events',
                queryset=Event.objects.order_by('start'),
                to_attr='all_participations',
            )
        )

    def with_all_affiliations(self):
        return self.prefetch_related(
            Prefetch(
                'institutes',
                queryset=Institute.objects.order_by('affiliation__start'),
                to_attr='all_affiliations',
            )
        )

    def with_current_affiliations(self, date):
        return self.prefetch_related(
            Prefetch(
                'institutes',
                queryset=Institute.objects.filter(
                    (Q(affiliation__start__lte=date) | Q(affiliation__start=None)) & (Q(affiliation__end__gte=date) | Q(affiliation__end=None))
                ).distinct(),
                to_attr='current_affiliations',
            ),
        )

    def for_event(self, event_code):
        return self.filter(events__code=event_code)

    def with_full_name(self):
        return self.annotate(full_name=Concat('last_name', Value(', '), 'first_name'))


class ParticipantManager(UserManager.from_queryset(ParticipantQuerySet)):
    def get_queryset(self):
        return super().get_queryset().annotate(full_name=Concat('last_name', Value(', '), 'first_name'))


class Participant(AbstractUser):
    """
        Overrides the built-in Django User model and adds affiliations and workshop participations
    """
    class Meta:
        ordering = ['last_name', 'first_name']

    objects = ParticipantManager()

    institutes = models.ManyToManyField(
        'Institute',
        through='Affiliation',
        related_name = 'people',
    )
    events = models.ManyToManyField(
        'Event',
        through='Participation',
        related_name = 'participants',
    )
    about = models.TextField(blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
