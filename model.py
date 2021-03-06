from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import Flask, json, jsonify, request, render_template
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import requests
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from flask_cors import CORS
pd.options.mode.chained_assignment = None 


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
def index():
    return render_template('Website.html')

@app.route('/',methods=['POST'])
def do():
    a1=request.form['city']
    a2=request.form['add']
    a3=request.form['nec']
    a4=request.form['g']
    print("coolpa:",a1)
    address=a2
    city=a1
    print(a4)
    if a4=='':
        number=4
    else:
        number=int(a4)
    features=a3
    if a3=='':
        features=''
    R=6373.0#Earth's Radius
    api='4519d076b432f5'
    hotel_details=pd.read_csv('Hotel_details.csv',delimiter=',')
    hotel_rooms=pd.read_csv('Hotel_Room_attributes.csv',delimiter=',')
    hotel_cost=pd.read_csv('hotels_RoomPrice.csv',delimiter=',')
    del hotel_details['id']
    del hotel_rooms['id']
    del hotel_details['zipcode']
    hotel_details=hotel_details.dropna()
    hotel_rooms=hotel_rooms.dropna()
    hotel_details.drop_duplicates(subset='hotelid',keep=False,inplace=True)
    hotel=pd.merge(hotel_rooms,hotel_details,left_on='hotelcode',right_on='hotelid',how='inner')
    optimum_band=pd.read_csv('hotel_price_min_max - Formula.csv',delimiter=',')
    del hotel['hotelid']
    hotel['url']
    del hotel['curr']
    del hotel['Source']
    sw = stopwords.words('english')
    lemm = WordNetLemmatizer()
    url = "https://us1.locationiq.com/v1/search.php"
    hotel['roomamenities']=hotel['roomamenities'].str.replace(': ;',',')
    features_tokens=word_tokenize(features)
    f1_set = {w for w in features_tokens if not w in sw}
    f_set=set()
    for se in f1_set:
        f_set.add(lemm.lemmatize(se))
    data = {
    'key': api,
    'q': address,
    'format': 'json'}
    response = requests.get(url, params=data)
    dist=[]
    lat1,long1=response.json()[0]['lat'],response.json()[0]['lon']
    lat1=radians(float(lat1))
    long1=radians(float(long1))
    hybridbase=hotel
    #hybridbase=hotel[hotel['guests_no']==number]
    hybridbase['city']=hybridbase['city'].str.lower()
    hybridbase=hybridbase[hybridbase['city']==city.lower()]
    hybridbase.drop_duplicates(subset='hotelcode',inplace=True,keep='first')
    hybridbase=hybridbase.set_index(np.arange(hybridbase.shape[0]))
    for i in range(hybridbase.shape[0]):
        lat2=radians(hybridbase['latitude'][i])
        long2=radians(hybridbase['longitude'][i])
        dlon = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        dist.append(distance)
    hybridbase['distance']=dist
    hybridbase=hybridbase[hybridbase['distance']<=5]
    hybridbase=hybridbase.set_index(np.arange(hybridbase.shape[0]))
    coss=[]
    for i in range(hybridbase.shape[0]):
        temp_tokens=word_tokenize(hybridbase['roomamenities'][i])
        temp1_set={w for w in temp_tokens if not w in sw}
        temp_set=set()
        for se in temp1_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
        coss.append(len(rvector))
    hybridbase['similarity']=coss
    h=hybridbase.sort_values(by='similarity',ascending=False)
    price_band=pd.merge(h,optimum_band,left_on=['hotelcode'],right_on=['hotelcode'],how='inner')
    price_band=pd.merge(price_band,hotel_cost,left_on=['hotelcode'],right_on=['hotelcode'],how='inner')
    del price_band['min']
    del price_band['max']
    del price_band['Diff_Min']
    del price_band['Diff_Max']
    #del price_band['currency']
    del price_band['country']
    del price_band['propertytype']
    #del price_band['starrating']
    #del price_band['latitude']
    #del price_band['longitude']
    price_band=price_band[price_band['Score']<=0.5]
    price_band=price_band[price_band['maxoccupancy']>=number]
    price_band.drop_duplicates(subset='hotelcode',inplace=True,keep='first')
    d1=price_band
    
    d1=d1[['hotelname','distance','roomtype_x','address','city','onsiterate','maxoccupancy','currency','latitude','longitude','starrating','url']].head(10)
    print(d1)

    # html=d1.to_html()
    # text_file = open("templates\ind.html", "w")
    # text_file.write(html)
    # text_file.close()
    # return render_template("ind.html")
    return {'city':list(d1['city']),'address':list(d1['address']),
    'maxoccupancy':list(d1['maxoccupancy']),'latitude':list(d1['latitude']),'longitude':list(d1['longitude']),'roomtype_x':list(d1['roomtype_x']),'hotelname':list(d1['hotelname']),'onsiterate':list(d1['onsiterate']),
    'distance':list(d1['distance']),'starrating':list(d1['starrating']),'url':list(d1['url'])}
    

if __name__== '__main__':
    app.run(debug=True)
