from django.db import models
from login_api.models import UserModel
from venues.models import VenuesModel

class GamesModel(models.Model):
    WeekDay = models.CharField(max_length=10)
    Time=models.CharField(max_length=10)
    Director=models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    Venue=models.ForeignKey(VenuesModel, null=True, on_delete=models.PROTECT)
    Description=models.CharField(max_length=250, null=True)
    active=models.BooleanField(default=True)
    
    def GetText(self):

        return '{} - {} - {} - {}'.format(self.Venue.VenueName, self.WeekDay, self.Time, self.Description)