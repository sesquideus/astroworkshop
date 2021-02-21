from django.db import models


class Participation(models.Model):
    person = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='participants')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='attended_events')
    online = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        online = " [online]" if self.online else ""
        return f"{self.person} at {self.event}{online}"
