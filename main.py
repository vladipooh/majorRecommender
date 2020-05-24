import os
import flask
from flask import Flask, render_template, request, redirect, url_for
import pickle
import requests
from datetime import timedelta
from functools import update_wrapper

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

# loading my model
model = pickle.load(open("mbti.pkl", "rb"))

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('form.html')

@app.route('/test/', methods=['GET','POST'])
def predict():
    url = "https://majorrec.herokuapp.com/predict"
    data = {"feature_array": [1.0, 2.0, 1.0, 1.0, 3.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 4.0]}
    r = requests.post(url, json=data)
    return r.text

# defining a route for only post requests
@app.route('/predict/', methods=['POST'])
def index():
    # getting an array of features from the post request's body
    feature_array = request.get_json()['feature_array']

    # creating a response object
    # storing the model's prediction in the object
    response = {}
    response['predictions'] = model.predict([feature_array]).tolist()

    # returning the response object as json
    return flask.jsonify(response)


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()