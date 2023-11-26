from django.urls import path,include
from . import views
from .views import *

urlpatterns = [
    path('data/', data_api_view, name='data_list'),
    path('data/<int:pk>', data_detail_api_view, name='data_details'),
    path('dataD', data_detail_api_view, name='data_details'),
    path('dataDic/', data_dic_view, name='data_dic'),
    path('apiArroyo/', apiArroyo, name='arroyo'),
    path('procesa_arroyo/', procesa_arroyo, name='procesa')

]