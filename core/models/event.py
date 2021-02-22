from django.db import models


class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name
