from django.db import models


class Affiliation(models.Model):
    person = models.ForeignKey('Participant', on_delete=models.CASCADE)
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE, related_name='people')
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.person} at {self.institute}"
