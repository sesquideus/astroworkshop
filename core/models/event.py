from django.db import models


def event_filename(instance, filename):
    return f"event/{instance.code}/programme.pdf"


class Event(models.Model):
    class Meta:
        ordering = ('start', 'name')

    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pdf_programme = models.FileField(null=True, blank=True, upload_to=event_filename)

    def __str__(self):
        return self.name
