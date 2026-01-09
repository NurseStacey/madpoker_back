from django.db import models

class VenuesModel(models.Model):
    VenueName = models.CharField(max_length=50)
    active = models.BooleanField(default=True)