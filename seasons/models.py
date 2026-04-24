from django.db import models
from datetime import timedelta
from django.utils import timezone
from .utils import *
    
class SeasonTypeModel(models.Model):
    season_type = models.CharField(max_length=100, default='In Person')
  
    @classmethod
    def get_default(cls):
        pass
        season,created = cls.objects.get_or_create(
            season_type='In Person', 
        )
        return season
    
    @classmethod
    def get_default_pk(cls):
        pass
        season,created = cls.objects.get_or_create(
            season_type='In Person', 
        )
        return season.pk
    
class SeasonModel(models.Model):
    season=models.CharField(default=0)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=ThreeMonthsLater)
    season_type=models.ForeignKey(SeasonTypeModel, on_delete=models.SET_DEFAULT, default=SeasonTypeModel.get_default_pk)

