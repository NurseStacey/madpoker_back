from django.db import models
from datetime import date

class HomePageText(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(null=False)
    color = models.CharField(max_length=10, default='#0000DD')
    font_size = models.IntegerField(default=18)
    order  = models.IntegerField(null=True)

class SpecialMessages(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(null=False)
    color = models.CharField(max_length=10, default='#0000DD')
    font_size = models.IntegerField(default=18)
    date = models.DateField(default=date.today())
