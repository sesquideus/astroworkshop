from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=32, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
