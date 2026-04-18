from django.db import models

class VenueModel(models.Model):
    venue_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    display_label= models.CharField(max_length=100, default='')
    image = models.ImageField(blank=True, 
                              null=True,
                              upload_to='venue_pics/',
                              default='venue_pics/default.png',)
    
    def __repr__(self):
        return self.venue_name