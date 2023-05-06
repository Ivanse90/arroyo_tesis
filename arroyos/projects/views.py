import json
from django import http
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import History_Tweet
from django.http import JsonResponse

# Create your views here.

class HistoryView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        history = list(History_Tweet.objects.values())
        if len(history) > 0:
            datos = {'message':"Succes",'history':history}
        else:
            datos = {'message':"HIstory not found..."}
        return JsonResponse(datos)

    def post(self,request):
        jd = json.loads(request.body)
        print("****",jd)
        History_Tweet.objects.create(usertextwe=jd['usertextwe'])
        datos = {'message':"Succes"}
        return JsonResponse(datos)

    def put(self,request):
        pass

    def delete(self,request):
        pass