from django.db import models
from players.models import PlayerModel
from games.models import PlayedGameModel
from django.utils import timezone
from datetime import date

class GameResultModel(models.Model):
    player=models.ForeignKey(PlayerModel,  default=PlayerModel.get_default_pk, on_delete=models.PROTECT)
    position=models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    registration_date_time=models.DateTimeField(default=timezone.now)
    game=models.ForeignKey(PlayedGameModel, null=True, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'player'], name='unique_registration')
        ]

    def this_result_no_venue(self):
        return {
            'player':self.player.player,
            'position':self.position,
            'points':self.points
        }

    
    def this_result(self):
        game_info = self.game.get_dictionary_for_results_view()
        
        display_str= '{} - {} - Position:{} - Points:{}'.format(game_info['venue'],game_info['date'], self.position, self.points)
        
        return {
            'id':self.id,
            'position':self.position,
            'points':self.points,
            'display_str':display_str,
            'display_pieces':{
                'venue':game_info['venue'],
                'date':game_info['date'],
                'position':self.position,
                'points':self.points
            },
            'season':{
                'season_name':game_info['season'],
                'season_title':game_info['season'],
                'season_start_date':game_info['season_start_date'].strftime('%m-%d-%Y'),
                'season_start_index':(game_info['season_start_date']-date(2015,1,1)).days,
            }
        }