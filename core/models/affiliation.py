from django.db import models


class Affiliation(models.Model):
    class Meta:
        ordering = ['start']
        verbose_name = 'afiliácia'
        verbose_name_plural = 'afiliácie'

    person = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='affiliation', verbose_name='osoba')
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE, related_name='affiliation', verbose_name='inštitúcia')
    start = models.DateField(null=True, blank=True, verbose_name='začiatok')
    end = models.DateField(null=True, blank=True, verbose_name='koniec')

    def __str__(self):
        return f"{self.person} at {self.institute}"
