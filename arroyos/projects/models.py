from django.db import models

# Create your models here.

class History_Tweet(models.Model):
    #textwe = models.CharField(max_length = 200)
    #usuario_twe = models.CharField(max_length =30)
    usertextwe = models.CharField(max_length = 200)
    create_at = models.DateTimeField(auto_now = True)
    