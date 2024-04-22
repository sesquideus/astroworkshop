import datetime

from django.db import models
from django.db.models import Prefetch, F, Q, Value, Count
from django.db.models.functions import Concat
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from .slot import Slot
from .event import Event
from .affiliation import Affiliation
from .participation import Participation


class ParticipantQuerySet(models.QuerySet):
    def with_talks(self):
        return self.prefetch_related(
            Prefetch(
                'slots',
                queryset=Slot.objects.filter(
                    Q(category=Slot.CATEGORY_TALK) | Q(category=Slot.CATEGORY_WORKSHOP)
                ).order_by('event__start').with_event(),
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
                'affiliation',
                queryset=Affiliation.objects.order_by('start').select_related('institute'),
                to_attr='all_affiliations',
            )
        )

    def with_current_affiliations(self, date):
        return self.prefetch_related(
            Prefetch(
                'affiliation',
                queryset=Affiliation.objects.with_institute().filter(
                    Q(start__lte=date) | Q(start=None),
                    Q(end__gte=date) | Q(end=None)
                ).distinct(),
                to_attr='current_affiliations',
            ),
        )

    def with_participation_for_event(self, event_code):
        return self.prefetch_related(
            Prefetch(
                'participations',
                queryset=Participation.objects.filter(event__code=event_code),
                to_attr='current_participation',
            ),
        )

    def with_participations(self):
        return self.prefetch_related(
            Prefetch(
                'participations',
                queryset=Participation.objects.prefetch_related('event')
            ),
        ).annotate(total_participations=Count('participations'))

    def for_event(self, event_code):
        return self.filter(events__code=event_code)

    def with_full_name(self):
        return self.annotate(full_name=Concat('last_name', Value(', '), 'first_name'))


class ParticipantManager(BaseUserManager.from_queryset(ParticipantQuerySet)):
    def get_queryset(self):
        return super().get_queryset().annotate(full_name=Concat('last_name', Value(', '), 'first_name'))


class Participant(AbstractUser):
    """
    Overrides the built-in Django User model and adds affiliations and workshop participations
    """
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'účastník'
        verbose_name_plural = 'účastníci'

    objects = ParticipantManager()

    institutes = models.ManyToManyField('Institute', through='Affiliation', related_name='people')
    events = models.ManyToManyField('Event', through='Participation', related_name='participants')
    about = models.TextField(blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_full_name(self):
        return f"{self.last_name}, {self.first_name}"
    get_full_name.short_description = 'celé meno'

    def get_natural_name(self):
        return f"{self.first_name} {self.last_name}"

