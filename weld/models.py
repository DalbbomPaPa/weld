from django.db import models

# Create your models here.

class Weld_info(models.Model):
  model_name = models.CharField(max_length=10)
  program = models.CharField(max_length=10)
  power = models.IntegerField()
  freq = models.FloatField()
  length = models.FloatField()
  # selected = models.BooleanField()
  
  def __str__(self):
    return f'{self.id}, {self.model_name}'

class Weld_raw_data(models.Model):
  date = models.DateTimeField()
  model_id = models.IntegerField()
  model_name = models.CharField(max_length=10)
  before_result = models.BooleanField()
  after_result = models.BooleanField()
  result = models.BooleanField()
  power = models.IntegerField()
  freq = models.FloatField()
  length = models.FloatField()
  
  def __str__(self):
    return f'{self.date}, {self.model_name}'
