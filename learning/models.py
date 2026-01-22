from django.db import models

class TestingSectionModel(models.Model):
    section_name=models.CharField(max_length=20)

class TestingGameModel(models.Model):
    game_name=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    all_sections=models.ManyToManyField(TestingSectionModel,through='TestingSectionThrough', related_name='game_sections')

class TestingSectionThrough(models.Model):
    section=models.ForeignKey(TestingSectionModel, on_delete=models.PROTECT)
    game=models.ForeignKey(TestingGameModel, on_delete=models.PROTECT)
    director=models.CharField(max_length=20)
    active=models.BooleanField(default=True)  
    description=models.CharField(max_length=250, null=True)  
