from django.db import models
from login_api.models import UserModel
from venues.models import VenuesModel
from datetime import date
from players.models import PlayersModel


class GamesModel(models.Model):
    WeekDay = models.CharField(max_length=10)
    Time=models.CharField(max_length=10)
    Director=models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    Venue=models.ForeignKey(VenuesModel, null=True, on_delete=models.PROTECT)
    Description=models.CharField(max_length=250, null=True)
    active=models.BooleanField(default=True)
    

    def GetText(self):

        return '{} - {} - {} - {}'.format(self.Venue.VenueName, self.WeekDay, self.Time, self.Description)
    
    @classmethod
    def get_default_pk(cls):
        oneGame, created = cls.objects.get_or_create(
            Description='default game', 
            defaults={
                'WeekDay':'Monday',
                'Time':'5:00'
            },
        )
        return oneGame.pk    
    
class PlayedGamesModel(models.Model):
    WhichGame= models.ForeignKey(GamesModel, on_delete=models.PROTECT, default=GamesModel.get_default_pk)
    Date= models.DateField(default=date.today())
    Season=models.IntegerField(default=0)
    Players=models.ManyToManyField(PlayersModel,  default=PlayersModel.get_default_pk)