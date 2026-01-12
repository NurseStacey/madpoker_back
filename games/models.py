from django.db import models
from login_api.models import UserModel
from venues.models import VenuesModel
from datetime import date,timedelta
from players.models import PlayersModel


class SeasonsModel(models.Model):
    SeasonNumber=models.CharField(default=0)
    StartDate=models.DateField(default=date.today())


class GamesModel(models.Model):
    WeekDay = models.CharField(max_length=10)
    Time=models.CharField(max_length=10)
    Director=models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    Venue=models.ForeignKey(VenuesModel, null=True, on_delete=models.PROTECT)
    Description=models.CharField(max_length=250, null=True)
    active=models.BooleanField(default=True)
    

    def GetNextGameID(self):
        Today=date.today()
        next_game=self.game_details.all().order_by('-Date').first()

        if next_game==None or (next_game.Date-Today).days<0:
  
            today_weekday = (Today.weekday()+1 % 7) #0 is Monday here.  0 is Sunday in model


            PlayedGamesModel.create(
                WhichGame=self,
                Date = (date(Today.year, Today.month, Today.day)+timedelta(days=(self.WeekDay-today_weekday)))
            )

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
    WhichGame= models.ForeignKey(GamesModel, on_delete=models.PROTECT, default=GamesModel.get_default_pk, related_name='game_details')
    Date= models.DateField(default=date.today())
    Players=models.ManyToManyField(PlayersModel,  default=PlayersModel.get_default_pk)