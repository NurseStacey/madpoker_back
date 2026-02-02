from django.db import models
from datetime import timedelta
from django.utils import timezone
from .utils import *
    
class SeasonModel(models.Model):
    season=models.CharField(default=0)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=ThreeMonthsLater)
