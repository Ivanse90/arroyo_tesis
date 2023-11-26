from rest_framework import serializers
from .models import data_tweet,History_Tweet

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = data_tweet
        fields = '__all__'




class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History_Tweet
        fields = '__all__'