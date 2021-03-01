from django.db import models


class Participation(models.Model):
    person = models.ForeignKey('Participant', on_delete=models.CASCADE, null=False)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=False)
    online = models.BooleanField(null=False, blank=False, default=False)
    organizer = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        online = " [online]" if self.online else ""
        return f"{self.person} at {self.event}{online}"