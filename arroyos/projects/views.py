import json
from django import http
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import History_Tweet,data_tweet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DataSerializer,HistorySerializer 
from .api_arroyo import Arroyo,CallData,ProcessData,UseModelData
from datetime import datetime
from django.utils import timezone
import aiohttp
import asyncio



# Create your views here.


@api_view(['GET','POST'])
def data_api_view(request):
    """
    Api tipo Get,POST
    encargada de obtener e Insertar
    de eventos en la base de datos
    """
    if request.method == 'GET':
        data_tw = data_tweet.objects.all()
        data_serializer = DataSerializer(data_tw, many = True)
        return Response(data_serializer.data)
    elif request.method == 'POST':
        data_serializer = DataSerializer(data = request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response("Successful..., Post Completed")
        return Response(data_serializer.errors)

@api_view(['GET','PUT','DELETE'])
def data_detail_api_view(request,pk=None):
    """
    Api tipo Get,PUT, DELETE
    encargada de obtener,actualizar y eliminar datos
    de eventos en la base de datos
    """
    if request.method == 'GET':
        data_tw = data_tweet.objects.filter(id = pk).first()
        data_serializer = DataSerializer(data_tw)
        return Response(data_serializer.data)
    elif request.method == 'PUT':
        data_tw = data_tweet.objects.filter(id = pk).first()
        data_serializer = DataSerializer(data_tw, data = request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response("Successful..., PUT Completed")
        return Response(data_serializer.errors)
    
    elif request.method == 'DELETE':
        data_tw = data_tweet.objects.filter(id = pk).first()
        data_tw.delete()
        
        return Response("Successful..., DELETE Completed")

@api_view(['GET'])
def data_dic_view(request):
    """
    Api tipo Get
    encargada de obtener los arroyos y su cantidad de eventos
    desde la Base de datos
    """
    if request.method == 'GET':
        data_tw = data_tweet.objects.all()
        data_serializer = DataSerializer(data_tw, many = True)
        
        dic_val = Arroyo.dataFrame(data_serializer.data)
        intensity_arroyo = Arroyo.dic_arroyo(dic_val)
        response_arroyo =  Arroyo.arroyo_response(intensity_arroyo)
        return Response(response_arroyo)
    else:
        return Response(data_serializer.errors)



@api_view(['GET'])
def apiArroyo(request):
    """
    Api tipo Get
    encargada de obtener datos de twitter e insertarlos en la bd
    """
    desbor_obj = CallData.runData()
    conta = 0
    for i in range(len(desbor_obj[0])):
        conta += 1
        tweethis = {'id_data':conta,'tweet_text':str(desbor_obj[0][i]),'usertext':'Ivan'}
        history_serializer = HistorySerializer(data = tweethis)
        if history_serializer.is_valid():
            history_serializer.save()
    if history_serializer.is_valid():
        return Response("Successful..., TWEETWER DATA INSERT Completed")
    return Response(history_serializer.errors)


@api_view(['GET'])
def procesa_arroyo(request):
    """
    Api tipo Get
    encargada de procesar datos de evento de arroyo
    """
    data_ht = History_Tweet.objects.filter(checked=1)[:2]
    history_serializer = HistorySerializer(data_ht, many = True)
    listdata = UseModelData.data_list(history_serializer.data)

    lend = len(history_serializer.data)
    for ln in range(lend):
        
        ct = history_serializer.data[ln]["id"]
        hy_tw = History_Tweet.objects.filter(id = ct).first()
        date_t = history_serializer.data[ln]['create_at']
        text_t = history_serializer.data[ln]['tweet_text'] 
        body_check = {"usertext":"Ivan","create_at":date_t,"id_data":"1","tweet_text":text_t,"checked":"SI"}
        
        his_serializer = HistorySerializer(hy_tw, data = body_check)

        
        if his_serializer.is_valid():

            his_serializer.save()


    for jwrv in listdata:
        modeldata = UseModelData.use_model(jwrv)
        data_serializer = DataSerializer(data = modeldata)
        if data_serializer.is_valid():
            data_serializer.save()
    return Response("Successful..., Data Insert Completed")


