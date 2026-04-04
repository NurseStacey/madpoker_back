from django.db import models
from login_api.models import UserModel
from venues.models import VenueModel
from datetime import date,timedelta,datetime
from django.utils import timezone
from seasons.models import SeasonTypeModel,SeasonModel
from .utils import *
import re


class GameTypeModel(models.Model):
    name=models.CharField(max_length=20, default='Texas Holdem', unique=True)

    @classmethod
    def get_default_pk(cls):
        game_type,created = cls.objects.get_or_create(
            name='Texas Holdem', 
        )
        return game_type.pk
    
    def __repr__(self):
        return self.name
    
class GameModel(models.Model):
    week_day = models.CharField(max_length=10)
    time=models.CharField(max_length=10)
    venue=models.ForeignKey(VenueModel, null=True, on_delete=models.PROTECT)
    active=models.BooleanField(default=True)  
    director=models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    description=models.CharField(max_length=250, null=True, blank=True)
    season_type=models.ForeignKey(SeasonTypeModel,  on_delete=models.SET_DEFAULT,default=SeasonTypeModel.get_default_pk )
    game_type = models.ForeignKey(GameTypeModel,  on_delete=models.SET_DEFAULT, default=GameTypeModel.get_default_pk)
    
    def __repr__(self):
        return self.venue.venue_name + "-" + self.week_day

    def RosterDictionary(self):
        return_value={
            'venue':self.venue.venue_name,
            'title':'{}-{}-{}'.format(self.venue.venue_name,self.game_type.name,self.week_day),
            'director':self.director.username,
            'dates':[x.get_date_with_ID() for x in self.played_games.all()]
        }

        return return_value

    def GetNextPlayedGameInfo(self):
        Today=date.today()

        next_game=None
        try:
            next_game=self.played_games.all().latest('date')
        except:
            pass

        try:
            if next_game==None or next_game.finalized or (next_game.date-Today).days<0:
    
                today_weekday = (Today.weekday()+1 % 7) #0 is Monday here.  0 is Sunday in model

                offset=WeekDayNumbers[self.week_day]-today_weekday
                if offset<0:
                    offset+=7

                next_game = PlayedGameModel(
                    which_game=self,
                    date = (date(Today.year, Today.month, Today.day)+timedelta(days=offset))
                )
                next_game.save()
        except Exception as e:
            print(e)
        
        return {
            #'description':self.description,
            'description':self.create_description_array(),
            'id':self.id, 
            'played_game_id':next_game.id,
            'date':next_game.date.strftime('%m-%d'),
            'venue_name':self.venue.venue_name,
            'game_type':self.game_type.name,
            'time':self.time
        }            
    
    def create_description_array(self):
        return_value=[]
        description=self.description
        if description[:2]!='@@':
            description = '@@black@@' + description

        if description[-2:]!='@@':
            description=description+'@@'

        temp_array=[]

        matches = list(re.finditer('@@', description))
        
        for one_match in [(matches[x],matches[x+1]) for x in range(len(matches)-1)]:
            temp_array.append(description[one_match[0].end():one_match[1].start()])

        temp_array_two=zip(temp_array[::2], temp_array[1::2])
        for index,one_piece in enumerate(temp_array_two):
            return_value.append({
                'color':one_piece[0],
                'text':one_piece[1],
                'index':index
            })
        
        return return_value
    
    def dictionary_for_location_page(self):

        return{
                'venue_name':self.venue.venue_name,   
                'description':self.description,             
                #'sections':[],
                'time':self.time,
                'date':1
            }
    
    def get_dates(self):
        datelist = [{'date':x.date,'id':x.id} for x in self.played_games.all()]
        datelist.sort(key=lambda x: x['date'], reverse=True)
        return [{'date':x['date'].strftime('%m-%d'),'id':x['id']} for x in datelist]

    def get_simple_text(self):
        return('{} - {}'.format(self.venue.venue_name, self.week_day))


    def GetText(self):
        try:

            return '{} - {} - {} - {} '.format(self.venue.venue_name, self.week_day,self.time, self.game_type.name)
        except:
            return 'default'
    
    @classmethod
    def get_default_pk(cls):
        oneGame, created = cls.objects.get_or_create(
            description='default game', 
            defaults={
                'WeekDay':'Monday',
                'Time':'5:00'
            },
        )
        return oneGame.pk    

class CanceledGamesModel(models.Model):
    which_game= models.ForeignKey(GameModel, 
                                on_delete=models.CASCADE, 
                                null=True, 
                                related_name='canceled_games')
    date=models.DateField(default=timezone.now)

class PlayedGameModel(models.Model):
    which_game= models.ForeignKey(GameModel, 
                                  on_delete=models.PROTECT, 
                                  null=True, 
                                  related_name='played_games')
    date= models.DateField(default=timezone.now)
    season = models.ForeignKey(SeasonModel, 
                               null=True, 
                               on_delete=models.PROTECT, 
                               related_name='playedgame_season')
    finalized=models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):

        self.season=self.get_season_record()
        super(PlayedGameModel,self).save(*args,**kwargs)

    def get_week_day(self):
        return self.which_game.week_day
    
    def get_date_with_ID(self):
        return {'date':self.date.strftime('%m-%d-%Y'),'id':self.id}
    
    def get_venue_name(self):
        return self.which_game.venue.venue_name
    
    def get_game_type(self):
        return self.which_game.game_type.name
    
    def get_dictionary_for_results_view(self):
        pass
        try:
            return({
                'venue':self.which_game.venue.venue_name,
                'date':self.date.strftime('%m/%d/%Y'),
                'season':self.get_season(),
                'season_start_date':self.get_season_start_date(),
                #'section':self.which_game.section.name,
                'id':self.id
            })
        except Exception as e:
            print(e)
            return({})
    
    def get_season_start_date(self):
        this_season_type=self.which_game.season_type
        
        try:
            this_season=SeasonModel.objects.filter(
            season_type=this_season_type).filter(
                start_date__lte=self.date).get(
                    end_date__gte=self.date
                )
        
            return this_season.start_date
        except:
            return date(2015,1,1)

    def get_season_record(self):
        this_season_type=self.which_game.season_type

        try:
            this_season=SeasonModel.objects.filter(
            season_type=this_season_type).filter(
                start_date__lte=self.date).get(
                    end_date__gte=self.date
                )
        
            return this_season
        except:
            return None
                            
    def get_season(self):
        this_season_type=self.which_game.season_type
        
        try:
            this_season=SeasonModel.objects.filter(
            season_type=this_season_type).filter(
                start_date__lte=self.date).get(
                    end_date__gte=self.date
                )
        
            return this_season.season
        except:
            return 'no associated season'

    def get_other_events(self):

        sections_this_date = PlayedGameModel.objects.filter(date=self.date)
        the_game=self.which_game.game
        these_sections = [x for x in sections_this_date if x.which_game.game==the_game and x.which_game.section!=self.which_game.section]
        return_value=[{'event_name':x.which_game.section.name,'id':x.id } for x in these_sections]

        return return_value
    
    def __repr__(self):
        return self.date.strftime('%m-%d')
    
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
    