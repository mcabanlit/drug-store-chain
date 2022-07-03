import pandas as pd
from flask import Flask, request, jsonify
import pickle
from datetime import datetime

from pywebio.platform.flask import webio_view
from pywebio.input import *
from pywebio.output import *



app = Flask(__name__)

stores_df = pd.read_csv("data/store_details.csv")
validation_empty = pd.read_csv("data/validation_empty.csv")
model = pickle.load(open('sales_prediction_lite.pkl', 'rb'))


@app.route('/')
def index():
    """
    Index of our app, which basically just says to access the API via /predict
    """
    return 'Access the API via /predict'


@app.route('/<name>')
def print_name(name):
    """
    Prints the name being passed.
    """
    return 'Hi, {}'.format(name)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Requests JSON to be passed to our prediction function.
    """

    if request.method == 'GET':
        return 'Access the API via POST request.'

    if request.method == 'POST':
        content = request.get_json(silent=True)
        result = predict_sales(content)
        return result


def check_null_features(input):
    """
    Checks for the completeness of the passed JSON.

    Parameters
    ----------
    input : Dictionary
        A dictionary of the values sent in the user request.

    Returns
    -------
    null_fields int
        The number of fields that are missing.
    """

    null_fields = 0
    required_fields = ["Store", "DayOfWeek", "Date", "Customers", "Open", "Promo", "StateHoliday","SchoolHoliday"]
    for field in required_fields:
        if not input.__contains__(field):
            null_fields = null_fields + 1
    return null_fields


def predict_sales(input):
    """
    Predicts the sales given the required fields from passed JSON.

    Parameters
    ----------
    input : Dictionary
        A dictionary of the values sent in the user request.

    Returns
    -------
    jsonify(key=value) string
        For most cases, would be the sales forecast but if there are errors, then it would return the error.
    """

    # Values that are being fed to a model, for reference purposes only.
    # values = [[353,4,1070,1,0,1,1,2015,1,1,1,1,1,900.0,8.0,2010.0,1,14.0,2013.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,0.0]]

    # Check if all the required fields have been filled out.
    null_fields = check_null_features(input)
    if null_fields > 0:
        return jsonify(ERROR='Missing input values, please recheck JSON file.')

    # Checks if the store passed, exists in our store dataset.
    current_store = stores_df[stores_df.Store == input["Store"]]
    if len(current_store) != 1:
        return jsonify(ERROR='Invalid store ID.')

    # Checks if the date passed, is in the expected format.
    a_date = input["Date"]
    res = True
    try:
        res = bool(datetime.strptime(a_date, '%Y-%m-%d'))
    except ValueError:
        res = False

    if not res:
        return jsonify(ERROR='Invalid Date Format. Must be YYYY-MM-DD')
    else:
        format_date = datetime.strptime(input["Date"], '%Y-%m-%d')

    # Creates a dictionary of all the values required by our model
    # Assumes correct format.
    values = {
        "Store": input["Store"],
        "DayOfWeek": input["DayOfWeek"],
        "Customers": input["Customers"],
        "Open": input["Open"],
        "Promo": input["Promo"],
        "StateHoliday": input["StateHoliday"],
        "SchoolHoliday": input["SchoolHoliday"],
        "SaleYear": format_date.year,
        "SaleMonth": format_date.month,
        "SaleDay": format_date.day,
        "SaleDayOfYear": format_date.timetuple().tm_yday,
        "StoreType": current_store["StoreType"],
        "Assortment": current_store["Assortment"],
        "CompetitionDistance": current_store["CompetitionDistance"],
        "CompetitionOpenSinceMonth": current_store["CompetitionOpenSinceMonth"],
        "CompetitionOpenSinceYear": current_store["CompetitionOpenSinceYear"],
        "Promo2": current_store["Promo2"],
        "Promo2SinceWeek": current_store["Promo2SinceWeek"],
        "Promo2SinceYear": current_store["Promo2SinceYear"],
        "PromoIntervalJan": current_store["PromoIntervalJan"],
        "PromoIntervalFeb": current_store["PromoIntervalFeb"],
        "PromoIntervalMar": current_store["PromoIntervalMar"],
        "PromoIntervalApr": current_store["PromoIntervalApr"],
        "PromoIntervalMay": current_store["PromoIntervalMay"],
        "PromoIntervalJun": current_store["PromoIntervalJun"],
        "PromoIntervalJul": current_store["PromoIntervalJul"],
        "PromoIntervalAug": current_store["PromoIntervalAug"],
        "PromoIntervalSep": current_store["PromoIntervalSep"],
        "PromoIntervalOct": current_store["PromoIntervalOct"],
        "PromoIntervalNov": current_store["PromoIntervalNov"],
        "PromoIntervalDec": current_store["PromoIntervalDec"],
    }

    # Convert our dictionary into a dataframe.
    for_prediction = pd.DataFrame.from_records([values])

    # Predict
    forecasted_sales = model.predict(for_prediction)
    print(forecasted_sales)
    forecasted_sales = float(forecasted_sales)

    # Return the forecasted value.
    return jsonify(sales=forecasted_sales)

#
# def welcome():
#     """
#     Sales Forecast
#     Predicts the sales given the required fields from user input.
#    """
#     put_text("")
#     welcome = input_group('What would you like to do?', [
#         actions('This web app uses Random Forest classifier on sales data in order '
#                 'to try and predict sales. Please choose one of the options below to proceed.', [
#                     {'label': 'Predict Sales', 'value': 'make_prediction', 'color': 'info'},
#                     {'label': 'View Documentation', 'value': 'view_dataset', 'color': 'secondary'},
#                     {'label': 'Browse Code', 'value': 'browse_code', 'color': 'dark'},
#                 ], name='action',
#                 help_text='The links above are only granted to key personnel, if you would like access, please '
#                           'feel free to email mcabanlitph@gmail.com'),
#     ])
#
#
# app.add_url_rule('/', 'webio_view', webio_view(welcome),
#                  methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    app.run()