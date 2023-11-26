from django.db import models

# Create your models here.

class History_Tweet(models.Model):
    usertext = models.CharField(max_length = 200)
    id_data = models.CharField(max_length = 200)
    tweet_text = models.CharField(max_length = 200)
    checked = models.CharField(max_length = 10)
    create_at = models.DateTimeField(auto_now = True)

class data_tweet(models.Model):
    tweet = models.CharField(max_length = 200)
    direccion_tweet = models.CharField(max_length = 200)   
    latitud =  models.CharField(max_length = 200)  
    longitud =  models.CharField(max_length = 200)  
