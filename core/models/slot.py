import unicodedata
import datetime

from django.apps import apps
from django.db import models
from django.db.models import Count, Prefetch, F, Subquery, OuterRef


def presentation_filename(instance, filename):
    return f"{instance.event.code}/{instance.id}/{filename}"


class SlotQuerySet(models.QuerySet):
    def with_people(self):
        Participant = apps.get_model('core', 'Participant')

        return self.prefetch_related(
            Prefetch(
                'person',
                queryset=Participant.objects.
                    with_current_affiliations(F("start")).
                    with_full_name(),
                to_attr='people',
            )
        ).annotate(
            people_count=Count('person'),
        )

    def with_event(self):
        return self.select_related('event')


class Slot(models.Model):
    class Meta:
        ordering = ['start', 'duration']
        verbose_name = 'slot'
        verbose_name_plural = 'sloty'

    objects = SlotQuerySet.as_manager()

    CATEGORY_TALK = 'T'
    CATEGORY_WORKSHOP = 'W'
    CATEGORY_MEAL = 'M'
    CATEGORY_OTHER = 'O'

    CATEGORIES = [
        (CATEGORY_TALK, 'Prednáška'),
        (CATEGORY_WORKSHOP, 'Workshop'),
        (CATEGORY_MEAL, 'Jedlo'),
        (CATEGORY_OTHER, 'Ostatné'),
    ]

    title = models.CharField(blank=True, max_length=256, verbose_name='názov')
    abstract = models.TextField(blank=True, max_length=4096, verbose_name='abstrakt')
    start = models.DateTimeField(null=True, blank=True, verbose_name='začiatok')
    duration = models.PositiveIntegerField(null=False, verbose_name='dĺžka (min)')
    note = models.CharField(blank=True, max_length=256, verbose_name='poznámka')
    person = models.ManyToManyField('Participant', related_name='slots', blank=True, verbose_name='účastník')
    event = models.ForeignKey('Event', null=True, blank=True, related_name='slots', on_delete=models.CASCADE,
                              verbose_name='workshop')
    category = models.CharField(max_length=1, choices=CATEGORIES, default=CATEGORY_TALK, verbose_name='kategória')
    online = models.BooleanField(null=False, blank=False, default=False, verbose_name='online')
    presentation = models.FileField(
        null=True,
        blank=True,
        upload_to=presentation_filename,
        verbose_name='prezentácia (PDF)'
    )
    video = models.URLField(max_length=100, null=True, blank=True, verbose_name='URL videa')

    def __str__(self):
        return f"{self.title} ({self.start})"

    def sorted_authors(self):
        return sorted(
            self.people, key=lambda x: unicodedata.normalize('NFKD', x.last_name)
        )
