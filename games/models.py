from django.db import models
from login_api.models import UserModel
from venues.models import VenueModel
from datetime import date,timedelta,datetime
from django.utils import timezone
from players.models import PlayerModel

WeekDayNumbers ={
    'Sunday':7,
    'Monday':1,
    'Tuesday':2,
    'Wednesday':3,
    'Thursday':4,
    'Friday':5,
    'Saturday':6
}

class SeasonModel(models.Model):
    season_number=models.CharField(default=0)
    start_date=models.DateField(default=timezone.now)

class SectionModel(models.Model):
    name=models.CharField(max_length=20, default='Texas Holdem', unique=True)

class GameModel(models.Model):
    week_day = models.CharField(max_length=10)
    time=models.CharField(max_length=10)
    venue=models.ForeignKey(VenueModel, null=True, on_delete=models.PROTECT)
    all_sections=models.ManyToManyField(SectionModel,through='SectionThrough', related_name='game_sections')
    active=models.BooleanField(default=True)  

    def get_dates(self):
        datelist = [{'date':x.date,'id':x.id} for x in self.game_details.all()]
        datelist.sort(key=lambda x: x['date'], reverse=True)
        return [{'date':x['date'].strftime('%m-%d'),'id':x['id']} for x in datelist]

    def get_simple_text(self):
        return('{} - {}'.format(self.venue.venue_name, self.week_day))
    
    def GetNextGameID(self):
        Today=date.today()
        next_game=self.game_details.all().order_by('-date').first()

        if next_game==None or (next_game.date-Today).days<0:
  
            today_weekday = (Today.weekday()+1 % 7) #0 is Monday here.  0 is Sunday in model

            offset=WeekDayNumbers[self.week_day]-today_weekday
            if offset<0:
                offset+=7

            next_game = PlayedGameModel(
                which_game=self,
                date = (date(Today.year, Today.month, Today.day)+timedelta(days=offset))
            )
            next_game.save()
        
        return next_game.id

    def GetText(self):
        try:

            return '{} - {} - {} '.format(self.venue.venue_name, self.week_day,self.time)
        except:
            return 'default'
    
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

class SectionThrough(models.Model):
    section=models.ForeignKey(SectionModel, on_delete=models.PROTECT)
    game=models.ForeignKey(GameModel, on_delete=models.PROTECT)
    director=models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    active=models.BooleanField(default=True)  
    description=models.CharField(max_length=250, null=True)  

class GameResultModel(models.Model):
    player=models.ForeignKey(PlayerModel,  default=PlayerModel.get_default_pk, on_delete=models.PROTECT)
    position=models.IntegerField(default=-1)
    registration_date_time=models.DateTimeField(default=timezone.now)

class PlayedGameModel(models.Model):
    which_game= models.ForeignKey(GameModel, on_delete=models.PROTECT, default=GameModel.get_default_pk, related_name='game_details')
    date= models.DateField(default=timezone.now)
    player_results=models.ManyToManyField(GameResultModel)
    #players=models.ManyToManyField(PlayerModel,  default=PlayerModel.get_default_pk)

    def get_players(self):

        return_value=[]
        for onePlayer in self.player_results.all():
            position_text=''
            if onePlayer.position>0:
                position_text=onePlayer.position

            return_value.append({
                'id':onePlayer.id,
                'name':onePlayer.player.player,
                'registration_time':timezone.localtime(onePlayer.registration_date_time).strftime('%m-%d  %H:%M'),
                'position':position_text
            })

        return return_value
    
