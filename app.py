from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory, jsonify
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server
import pywebio
import pickle
import numpy as np
from pywebio import STATIC_PATH
import pandas as pd

model = pickle.load(open('sales_prediction.pkl', 'rb'))
app = Flask(__name__)

# @app.route("/")
def predict():
    welcome = input_group('What would you like to do?', [
        actions('This web app uses Random Forest classifier on more than a thousand datasets on heart-disease in order '
                'to try and predict if a user has heart disease. Please choose one of the options below to proceed.', [
                    {'label': 'Check for Heart Disease', 'value': 'make_prediction', 'color': 'info'},
                    {'label': 'View Dataset', 'value': 'view_dataset', 'color': 'secondary'},
                    {'label': 'Browse Code', 'value': 'browse_code', 'color': 'dark'},
                ], name='action',
                help_text='This model uses factors such as age, sex, chest pain, blood pressure, serum '
                          'cholesterol, fasting blood sugar, resting ecg, maximum heart rate, exercise'
                          'induced angina and number of major vessels among others.'),
    ])
    # return jsonify(data="Hello from wtf.")

# @app.route("/predict", methods='POST')
# def dummy_api():
#     return jsonify(data="Hello from me.",
#                    tae="boto")

app.add_url_rule('/main', 'webio_view', webio_view(predict),
                 methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)

# if __name__ == '__main__':
#     # parser = argparse.ArgumentParser()
#     # parser.add_argument("-p", "--port", type=int, default=8080)
#     # args = parser.parse_args()
#     #
#     # start_server(dummy_api, port=args.port)
#     app.run()