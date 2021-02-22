from django.db import models


class Slot(models.Model):
    class Meta:
        ordering = ['start', 'person']

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

    title = models.CharField(null=True, blank=True, unique=True, max_length=256)
    abstract = models.TextField(null=True, blank=True, max_length=4096)
    start = models.DateTimeField(null=True, blank=True, unique=True)
    duration = models.PositiveIntegerField(null=False)
    person = models.ForeignKey('Participant', on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=CATEGORIES, default=CATEGORY_TALK)

    def __str__(self):
        return f"{self.person}: {self.title} ({self.start})"
