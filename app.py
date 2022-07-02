import flask
from flask import request, jsonify
# from flask import Flask, send_from_directory, jsonify

import pickle
import numpy as np
import pandas as pd

model = pickle.load(open('sales_prediction.pkl', 'rb'))
app = flask.Flask(__name__)

@app.route("/predict", methods=['GET'])
def predict():
    arg = request.args['arg']
    return jsonify(data="Hello from wtf.")
