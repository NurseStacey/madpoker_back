from django.db import models
from login_api.models import UserModel
from venues.models import VenueModel
from datetime import date,timedelta,datetime
from django.utils import timezone
from seasons.models import SeasonTypeModel,SeasonModel
from .utils import *

# class SectionModel(models.Model):
#     name=models.CharField(max_length=20, default='Texas Holdem', unique=True)

#     @classmethod
#     def get_default_pk(cls):
#         section,created = cls.objects.get_or_create(
#             name='Texas Holdem', 
#         )
#         return section.pk
    
#     def __repr__(self):
#         return self.name
    
class GameModel(models.Model):
    week_day = models.CharField(max_length=10)
    time=models.CharField(max_length=10)
    venue=models.ForeignKey(VenueModel, null=True, on_delete=models.PROTECT)
    #all_sections=models.ManyToManyField(SectionModel,through='SectionThrough', related_name='game_sections')
    active=models.BooleanField(default=True)  
    director=models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    description=models.CharField(max_length=250, null=True, blank=True)
    season_type=models.ForeignKey(SeasonTypeModel,  on_delete=models.SET_DEFAULT,default=SeasonTypeModel.get_default_pk )

    def __repr__(self):
        return self.venue.venue_name + "-" + self.week_day
    
    def dictionary_for_location_page(self):
        return{
                'venue_name':self.venue.venue_name,                
                #'sections':[],
                'time':self.time,
            }
    
    def get_dates(self):
        datelist = [{'date':x.date,'id':x.id} for x in self.game_details.all()]
        datelist.sort(key=lambda x: x['date'], reverse=True)
        return [{'date':x['date'].strftime('%m-%d'),'id':x['id']} for x in datelist]

    def get_simple_text(self):
        return('{} - {}'.format(self.venue.venue_name, self.week_day))


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

# class SectionThrough(models.Model):
#     section=models.ForeignKey(SectionModel, on_delete=models.PROTECT, default=SectionModel.get_default_pk)
#     game=models.ForeignKey(GameModel, on_delete=models.PROTECT)
#     director=models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
#     active=models.BooleanField(default=True)  
#     description=models.CharField(max_length=250, null=True, blank=True)

#     def need_to_protect(self):

#         try:
#             if len(PlayedGameModel.objects.filter(which_game=self))==0:
#                 return False
#             for onePlayedGame in PlayedGameModel.objects.filter(which_game=self):
#                 if onePlayedGame.date<date.today() and len(onePlayedGame.player_results.all()):
#                     return True
            
#             return False
#         except Exception as e:
#             print(e)

    
#     def GetNextPlayedGameInfo(self):
#         Today=date.today()

#         next_game=None
#         try:
#             next_game=self.played_games.all().latest('date')
#         except:
#             pass

#         # if next_game.finalized:
#         #     next_game = PlayedGameModel(
#         #         which_game=self,
#         #         date = (next_game.date+timedelta(days=offset))
#         #     )
#         #     next_game.save()

#         if next_game==None or next_game.finalized or (next_game.date-Today).days<0:
  
#             today_weekday = (Today.weekday()+1 % 7) #0 is Monday here.  0 is Sunday in model

#             offset=WeekDayNumbers[self.game.week_day]-today_weekday
#             if offset<0:
#                 offset+=7

#             next_game = PlayedGameModel(
#                 which_game=self,
#                 date = (date(Today.year, Today.month, Today.day)+timedelta(days=offset))
#             )
#             next_game.save()
        
#         return {
#             'description':self.description,
#             'id':self.id,
#             'event':self.section.name,            
#             'played_game_id':next_game.id,
#             'date':next_game.date.strftime('%m-%d')
#         }        


class PlayedGameModel(models.Model):
    which_game= models.ForeignKey(GameModel, 
                                  on_delete=models.PROTECT, 
                                  null=True, 
                                  related_name='played_games')
    date= models.DateField(default=timezone.now)
    finalized=models.BooleanField(default=False)
    
    def get_venue_name(self):
        return self.which_game.game.venue.venue_name
    
    def get_dictionary_for_results_view(self):
        pass
        try:
            return({
                'venue':self.which_game.game.venue.venue_name,
                'date':self.date,
                'season':self.get_season(),
                'section':self.which_game.section.name,
                'id':self.id
            })
        except Exception as e:
            print(e)
            return({})
    
    def get_season(self):
        this_season_type=self.which_game.game.season_type
        this_season=SeasonModel.objects.filter(
            season_type=this_season_type).filter(
                start_date__lte=self.date).get(
                    end_date__gte=self.date
                )
        return this_season.season

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