import datetime
from django.apps import apps
from django.db import models
from django.db.models import Prefetch

from . import Slot


def event_filename(instance, filename):
    return f"event/{instance.code}/programme.pdf"


class EventQuerySet(models.QuerySet):
    def with_slots(self):
        return self.prefetch_related(Prefetch(
            'slots',
            queryset=Slot.objects.with_people(),
        ))

    def with_participants(self):
        Participant = apps.get_model('core.Participant')
        return self.prefetch_related(Prefetch(
            'participants',
            queryset=Participant.objects.with_current_affiliations(datetime.date.today()),
        ))

    def only_visible(self):
        return self.filter(visible=True)


class Event(models.Model):
    class Meta:
        ordering = ('start', 'name')
        verbose_name = 'workshop'
        verbose_name_plural = 'workshopy'

    objects = EventQuerySet.as_manager()

    code = models.CharField(max_length=32, unique=True, verbose_name='kód')
    name = models.CharField(max_length=32, unique=True, verbose_name='názov')
    start = models.DateTimeField(verbose_name='začiatok')
    end = models.DateTimeField(verbose_name='koniec')
    visible = models.BooleanField()
    pdf_programme = models.FileField(null=True, blank=True, upload_to=event_filename, verbose_name='program (PDF)')

    def __str__(self):
        return self.name
