from django.db import models


class Institute(models.Model):
    class Meta:
        ordering = ['full_name']

    short_name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=256)

    def __str__(self):
        return self.short_name
