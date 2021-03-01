from django.db import models
from django.db.models import Count, Prefetch


class SlotQuerySet(models.QuerySet):
    def with_people(self):
        return self.prefetch_related(
            Prefetch('person', to_attr='people')
        ).annotate(
            people_count=Count('person')
        )


class Slot(models.Model):
    class Meta:
        ordering = ['start', 'duration']

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

    title = models.CharField(blank=True, max_length=256)
    abstract = models.TextField(blank=True, max_length=4096)
    start = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=False)
    note = models.CharField(blank=True, max_length=256)
    person = models.ManyToManyField('Participant', related_name='people', blank=True)
    event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=CATEGORIES, default=CATEGORY_TALK)

    def __str__(self):
        return f"{self.title} ({self.start})"
