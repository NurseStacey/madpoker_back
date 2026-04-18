from django.db import models

class VenueModel(models.Model):
    venue_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    image = models.ImageField(default='venue_pics/default.png',
                                     upload_to='venue_pics'),
    
    def __repr__(self):
        return self.venue_name