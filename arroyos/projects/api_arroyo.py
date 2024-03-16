import re
import requests
from .models import data_tweet
import os
import tweepy
import json
import psycopg2
from tweepy import cursor
import time
from datetime import date
import preprocess_kgptalkie as ps
import pickle
import re
import es_core_news_lg
import spacy
import pandas as pd
import geopandas as gpd





class Arroyo():

    def dic_arroyo(dicar):
        dic_arr = {}
        coount = 0
        for i in dicar.values.tolist():
            
            if i[0] in list(dic_arr.keys()):
                dic_arr[i[0]] = dic_arr.get(i[0]) + 1
            else:
                dic_arr[i[0]] = 1
        return dic_arr


    def arroyo_response(arroyo_dic):
        list_arr = []
        for ar in arroyo_dic:
            data = {"Arroyo":ar,
                    "Cantidad":arroyo_dic[ar]}
            list_arr.append(data)
        return list_arr

    
    def dataFrame(data):
        df = pd.DataFrame()
        df['Id_Tweet'] = None
        df['Lat_Tweet'] = None
        df['Long_Tweet'] = None
        corlat = []
        corlon = []

        for i in data:
            if i['latitud']:
                corlat.append(i['latitud'])
                corlon.append(i['longitud'])
        df['Lat_Tweet'] = corlat 
        df['Long_Tweet'] = corlon

        arroyo = f"../arroyos/projects/geo_data/ArroyoBarranquilla.geojson"
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Long_Tweet,df.Lat_Tweet))
        gdf = gdf.set_crs('epsg:4326')
        df_arroyo = gpd.read_file(open(arroyo))
        join_df = df_arroyo.sjoin(gdf, how="inner")
        df1 = pd.DataFrame(join_df.drop(columns='geometry'))
        df1['description'] = df1[['Name']]
        datos = df1[['description']]

        return datos
    

class CallData():

    def runData():
        
        #Autenticacion
        API_Key = "kj2ZBZ7NIrDUGbvo8hGSpxqOF"
        API_Key_Secret = "Qbqll1h12Gevi6On9m79e9lpYVCUjAHm2AdO9SjyMigWSlJIWu"

        access_token = "1430662532671410187-aWTsjOovhxCN1VT0Hp7p4D7Bcy8IeE"
        access_token_secret = "BXtIRXjASrkPXFZ144LvOfJMybpOxSQ6EGjXihmwzEkUo"

        Bearer_Token = "AAAAAAAAAAAAAAAAAAAAANexTAEAAAAAYwbca1kQWO9GaWAnHiZmqnY1PZQ%3DXXTjKbRbwdMZdMsWwO0GM2IFXj73XaZkF23S2500u24mcc48m0"
        Client = tweepy.Client(bearer_token=Bearer_Token,consumer_key=API_Key, consumer_secret=API_Key_Secret, 
                    access_token=access_token, access_token_secret=access_token_secret)
                    
        desbor = Client.search_all_tweets(query='point_radius:[-74.80263535515736 10.9780283806229 10km] "Arroyo"  OR "reportelluvia" retweets_of',
                max_results =200,
                start_time='2022-10-11T11:00:00Z',end_time='2023-03-11T19:54:59Z') 
        return desbor




class ProcessData():

    def get_vec(vc):
        npl = es_core_news_lg.load()
        doc = npl(vc)
        vec = doc.vector
        return vec

    def get_clean(X):
        X = str(X).lower().replace('\\','').replace('_',' ')
        X = ps.cont_exp(X)
        X = ps.remove_emails(X)
        X = ps.remove_urls(X)
        #X = ps.remove_html_tags(X)
        X = ps.remove_rt(X)
        X = ps.remove_accented_chars(X)
        X = ps.remove_special_chars(X)
        X = re.sub("(.)\\1{2,}","\\1",X)
        return X

    def geocode(addrt):
        API_KEY = 'AIzaSyAEwcRj0cJV_Z9viq-3cT8-RFfVsKUj-bw'
        if len(addrt) == 1:
            addrt.append("45                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ")
        ads = str(addrt[0]) + ' con' + str(addrt[1]) + ', Barranquilla, Atlantico, Colombia'
        parametros = {
            'key': API_KEY,
            'address':ads}
        base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

        response = requests.get(base_url, params=parametros).json()

        if response['status'] == 'OK':
            geom = response['results'][0]['geometry']
            lat = geom['location']['lat']
            lon = geom['location']['lng']
        return lat,lon


class UseModelData():

    def use_model(msj):
        arroyo_model = f"/home/user/Tesis/Back/Arroyo_back/arroyos/projects/geo_data/w2v_text_clasification_KNC.pkl"
        mdl = pickle.load(open(arroyo_model,'rb'))

        mensaje_t = ProcessData.get_clean(msj)
        vec_men = ProcessData.get_vec(msj)
        mdl_npl = mdl.predict(vec_men.reshape(1, -1))
        mdl_npl[0]
        if mdl_npl[0][0] == 1 and mdl_npl[0][1] == 0:
            m = re.findall('c\w*\s?\d{1,4}\s?', msj)

            if len(m)==0:
                mi = ['calle 85 ', 'carreras 50']
                resp = ProcessData.geocode(mi)
                print(msj + " ***SI ES UN EVENTO DE ARROYO**")
                return {"tweet":msj,"direccion_tweet":str(mi),"latitud":resp[0],"longitud":resp[1]}
            else:
                resp = ProcessData.geocode(m)
                print("tweet",msj,"direccion_tweet",str(m),"latitud",resp[0],"longitud",resp[1])
                print(msj + " ***SI ES UN EVENTO DE ARROYO**")
                return {"tweet":msj,"direccion_tweet":str(m),"latitud":resp[0],"longitud":resp[1]}
        else:
            print(msj + " ***NO ES UN EVENTO DE ARROYO**")
    
    def data_list(arrobj):
        list_arro = []
        for dt in range(len(arrobj)):
            list_arro.append(arrobj[dt]['tweet_text'])
        return list_arro


    
