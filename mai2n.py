import os
import pickle
import flask
import requests
from datetime import timedelta
from flask import make_response, request, current_app, render_template
from functools import update_wrapper
# from flask_cors import CORS

app = flask.Flask(__name__)
# cors = CORS(app)

# loading my model
model = pickle.load(open("mbti.pkl", "rb"))

@app.route('/')

def home():
   return render_template('form.html')

@app.route('/test', methods=['GET','POST'])
def predict():
        url = "/predict"
        data = {"feature_array": [1.0, 2.0, 1.0, 1.0, 3.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 4.0]}
        r = requests.post(url, json=data)
        return r.text

# defining a route for only post requests
@app.route('/predict', methods=['POST'])
def index():
    # getting an array of features from the post request's body
    feature_array = request.get_json()['feature_array']

    # creating a response object
    # storing the model's prediction in the object
    response = {}
    response['predictions'] = model.predict([feature_array]).tolist()

    # returning the response object as json
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)