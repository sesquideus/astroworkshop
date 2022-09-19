from django.db import models


class ParticipationQuerySet(models.QuerySet):
    def with_person(self):
        return self.select_related('person', 'event')


class Participation(models.Model):
    class Meta:
        ordering = ['event', 'person']

    objects = ParticipationQuerySet.as_manager()

    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=False)
    person = models.ForeignKey('Participant', on_delete=models.CASCADE, null=False, related_name='participations')
    online = models.BooleanField(null=False, blank=False, default=False)
    organizer = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        online = " [online]" if self.online else ""
        return f"{self.person} at {self.event}{online}"
