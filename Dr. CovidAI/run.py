from flaskblog import app
from flask_login import login_required
from flaskblog import bot
from flaskblog import pool

import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as k
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from flask import request,render_template
from flask import jsonify,make_response
from flask import Flask
import tensorflow as tf
import pandas as pd
import json


#from flask_ngrok import run_with_ngrok

#run_with_ngrok(app)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


def get_model(name):
	global modelnearby
	#modelnearby=load_model(name)
	print("MODEL LOADED!")
	return load_model(name,compile=False)

def preprocess_image(image,target_size):
	if image.mode!="RGB":
		image=image.convert("RGB")
	image=image.resize(target_size)
	image=img_to_array(image)
	image=np.expand_dims(image,axis=0)
	return image


print("LOADING KERAS COVID Xray Classification MODEL!")
cov_model=get_model("covid4.h5")
global cov_graph
cov_graph = tf.get_default_graph()



@app.route('/covidpredict', methods=["GET","POST"])
def covidpredict():
	message=request.get_json(force=True)
	encoded=message['image']
	#encoded=encoded+str("==")
	decoded=base64.b64decode(encoded)
	image=Image.open(io.BytesIO(decoded))
	processed_image=preprocess_image(image,target_size=(224,224))
	with cov_graph.as_default():
		prediction=cov_model.predict(processed_image)
		response={
		
		'c0':prediction[0][0],
		'c1':prediction[0][1],
		}
	return pd.Series(response).to_json(orient='values')

@app.route('/bothome')
def bothome():
	return render_template('bothome.html')

@app.route("/bothome/get")
def get_bot_response():
	userText = request.args.get('msg')
	return str(bot.get_response(userText))



if __name__ == '__main__':
    app.run(debug = True)