# Import flask which will handle our communication with the frontend
# Also import few other libraries
#from keras.models import load_model
#import tensorflow as tf
#import sys
#import os
# Path to our saved model
#sys.path.append(os.path.abspath("./model"))
#Initialize some global variables
#global graph
#model, graph = init()
#graph = tf.get_default_graph()

from keras import backend as K
#Before prediction
K.clear_session()


from flask import Flask, render_template, request
from scipy.misc import imread, imresize, imsave
import numpy as np
import re
import base64
import pickle
#import tensorflow as tf

# Initialize flask app
app = Flask(__name__)

def convertImage(imgData1):
	 imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
	 with open('output.png', 'wb') as output:
		   output.write(base64.b64decode(imgstr))

@app.route('/')
def index():
 return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
	 # Predict method is called when we push the 'Predict' button 
	 # on the webpage. We will feed the user drawn image to the model
	 # perform inference, and return the classification
     digit_detect_pkl = open('static/model/digit_predict.pkl', 'rb')
     model = pickle.load(digit_detect_pkl)
     #print(model)
     imgData = request.get_data()
     #print(imgData)
     #imgData = request.json
     convertImage(imgData)
	 # read the image into memory
     x = imread('output.png', mode='L')
	 # make it the right size
     x = imresize(x, (28, 28))/255
	 #You can save the image (optional) to view later
     imsave('final_image.jpg', x)
     x = x.reshape(1, 28, 28, 1)
     out = model.predict(x)
     response = np.argmax(out, axis=1)
     #After prediction
     K.clear_session()
     return str(response[0])
     

if __name__ == "__main__":
# run the app locally on the given port
	app.run(host='127.0.0.1', port=5000)

#vaidkunal.kv@gmail.com

#https://towardsdatascience.com/deploying-keras-deep-learning-models-with-flask-5da4181436a2
