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


class Event(models.Model):
    class Meta:
        ordering = ('start', 'name')

    objects = EventQuerySet.as_manager()

    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pdf_programme = models.FileField(null=True, blank=True, upload_to=event_filename)

    def __str__(self):
        return self.name
