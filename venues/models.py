from django.db import models

class VenueModel(models.Model):
    venue_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __repr__(self):
        return self.venue_name