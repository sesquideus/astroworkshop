from django.db import models


class Institute(models.Model):
    class Meta:
        ordering = ['full_name']
        verbose_name = 'inštitúcia'
        verbose_name_plural = 'inštitúcie'

    short_name = models.CharField(max_length=32, verbose_name='kód')
    full_name = models.CharField(max_length=256, verbose_name='plné meno')

    def __str__(self):
        return self.short_name
