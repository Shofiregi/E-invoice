from audioop import error
import flask_cors
from flask_cors import CORS
from flask import Config, Flask, render_template
# from flask_pymongo import PyMongo
from flask import jsonify, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import PIL
# from pymongo import MongoClient                      
# import keras
from werkzeug.utils import secure_filename
import io
from datetime import date, timedelta
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import imageio as iio
# import seaborn as sns
# sns.set_style('whitegrid')
from io import BytesIO
from PIL import Image
import base64
import statsmodels.api as sm


web_app=Flask(__name__)
# web_app.config['MONGO_URI'] = "mongodb://localhost:27017/fileupload"
# mongo=PyMongo(web_app)
CORS(web_app)

@web_app.route('/signup', methods=['POST'])
def signup():
        resp={}
        
        try:
            req_body = request.json
            print(req_body)
            p=req_body['file']
            q=request.form.get['duration']
            print(p)
            # mongo.db.file.insert_one(req_body)
             
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

@web_app.route('/image', methods=['POST'])
def send_file():
      img = Image.open("C:\\Users\\shiva\\KAAR PROJECT\\shivani.jpg")
      data = io.BytesIO()
      img.save(data, "JPEG")
      encoded_img_data = base64.b64encode(data.getvalue())
      return jsonify({'imageData':encoded_img_data.decode('utf-8')})

@web_app.route('/file_upload',methods=['POST'])
def fileUpload():
        resp = {}
        try:
            req = request.form
            file = request.files.get('file')
            
            # ML part using sarima(seasonal differencing)
       
            #     client.mydb.mycollection.insert_many(df)
            data = pd.read_csv(file)
            period="Year"
            count = 6
            data1=data     
            data1["Period"]= data1['datesold'].astype(str) +"-"+'01'
            data['datesold']=pd.to_datetime(data['datesold'],infer_datetime_format=True)
            data.set_index(['datesold'],inplace=True)
            data.sort_index(inplace=True)
            print(period)
            st=data1['Period'].iloc[-1]
            arr=list(map(int,st.split('-')))
            std = datetime(arr[0], arr[1], arr[2])
            if period=="Days":
                print("yes")
                new_date = std + timedelta(count)
                en=new_date.date()

            elif period=="Month":
                print("yes")
                new_date = std + relativedelta(months=+count)
                en=new_date.date()
		
            elif period=="Year":
                print("yes")
                new_date = std + relativedelta(years=+count)
                en=new_date.date()
            ts = data['price']
            df_shift = ts.diff(2).dropna()
            mod = sm.tsa.statespace.SARIMAX(df_shift, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False)
            results = mod.fit()
            p = [0] * count
            p[0] = data.iloc[-1][0]
            std = datetime(arr[0], arr[1], arr[2])
            p[1:] = results.predict(start=std, end=en)
            print(std.date())
            print(en)
            print(pd.DataFrame(p).cumsum())
            plt.plot(pd.DataFrame(p).cumsum())
            plt.ylabel('Price')
            plt.title('Price forecasting')
            plt.savefig('C:/Users/shiva/KAAR PROJECT/shivani/n.jpg')
            img = Image.open('C:/Users/shiva/KAAR PROJECT/shivani/n.jpg')
            plt.show()
            # data = io.BytesIO()
            # img.save(data, "JPEG")
            # encoded_img_data = base64.b64encode(data.getvalue())
            return jsonify()
            status = {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp



flask_cors.cross_origin(origins="*",method=['GET','POST','OPTIONS'],
supports_credentials=False,send_wildcard=True,automatic_options=True)



if __name__=="__main__":
    web_app.run(debug=True,port=5000)