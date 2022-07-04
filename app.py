import pandas as pd
from flask import Flask, request, jsonify
import pickle
from datetime import datetime

from pywebio.platform.flask import webio_view
from pywebio.input import *
from pywebio.output import *
import pywebio

app = Flask(__name__)

stores_df = pd.read_csv("data/store_details.csv")
validation_empty = pd.read_csv("data/validation_empty.csv")
model = pickle.load(open('sales_prediction_small.pkl', 'rb'))


@app.route('/faq')
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

    return 'Method Not Allowed'

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
    required_fields = ["Store", "DayOfWeek", "Date", "Customers", "Open", "Promo", "StateHoliday", "SchoolHoliday"]
    for field in required_fields:
        if not input.__contains__(field):
            null_fields = null_fields + 1
    return null_fields


def check_StateHoliday(value):
    """
    Converts the StateHoliday string to categorical values.

    Parameters
    ----------
    value : String
        The StateHoliday value sent in the user request.

    Returns
    -------
    category int
        Categorical equivalent of string to model
    """
    if value == "0":
        category = 0
    elif value == "a":
        category = 1
    elif value == "b":
        category = 2
    elif value == "c":
        category = 3
    else:
        category = -1

    return category

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

    # Check if string StateHoliday is correct.
    categorical_state_holiday = check_StateHoliday(input["StateHoliday"])
    if categorical_state_holiday < 0:
        return jsonify(ERROR='Invalid StateHoliday passed. Double check that it is a string with'
                             ' values in [0,a,b,c].')

    # Since sales_df.loc[(sales_df['Open'] == 0) & (sales_df['Sales'] > 0)] would return 0
    # We don't need to predict anymore since it should be zero.
    if input["Open"] == 0:
        return jsonify(sales=0.00)

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
        "StateHoliday": categorical_state_holiday,
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


def read_file(path):
    """
    Reads a text file

    Parameters
    ----------
    path : str
        Path of the file we want to read.

    Returns
    -------
    data string
        The text contained in the file.
    """
    # open text file in read mode
    text_file = open(path, "r")
    # read whole file to a string
    data = text_file.read()
    # close file
    text_file.close()

    return data


def welcome():
    """
    Sales Forecast
    Predicts the sales given the required fields from user input.
    """
    img = open('assets/banner.png', 'rb').read()
    # Ibrahim Rifath https://unsplash.com/photos/OApHds2yEGQ
    put_html("<h1>Sales Forecast API </h1>"
             "Please access '/predict' for forecasting sales. You may use postman as seen on the image below or"
             " you may import requests in your code.")
    put_text("")
    with use_scope('scope1', clear=True):
        put_image(img)
    put_text("")

    # Two code blocks of equal width, separated by 10 pixels

    code_a = read_file("assets/code1.txt")
    code_b = read_file("assets/code2.txt")

    put_row([put_code(code_a), None, put_code(code_b)])

    put_link("Github", "https://github.com/mcabanlit/drug-store-chain")

    # Commented out for future usage
    # user_actions = input_group('What would you like to do?', [
    #     actions('This web app uses Random Forest classifier on sales data in order '
    #             'to try and predict sales. Please choose one of the options below to proceed.', [
    #                 {'label': 'Predict Sales', 'value': 'make_prediction', 'color': 'info'},
    #                 {'label': 'View Documentation', 'value': 'view_dataset', 'color': 'secondary'},
    #                 {'label': 'Browse Code', 'value': 'browse_code', 'color': 'dark'},
    #             ], name='action',
    #             help_text='The links above are only granted to key personnel, if you would like access, please '
    #                       'feel free to email mcabanlitph@gmail.com'),
    # ])
    # if user_actions['action'] == 'make_prediction':
    #     accept = actions('Do you consent the processing of your data?', [
    #         # 'Yes', 'No'
    #         {'label': 'Yes, I consent.', 'value': 'i_consent', 'color': 'info'},
    #         {'label': 'No, I do not consent.', 'value': 'predict', 'color': 'dark'},
    #     ], help_text='We will not be storing any of the values that you have entered after the prediction. '
    #                  'Please also note that the results of this forecast are not final and is only a product of '
    #                  'a model that was trained using the given dataset.')
    #
    #     if accept == 'i_consent':
    #         put_text("")
    #         with use_scope('scope1', clear=True):
    #             put_text("")
    # elif user_actions['action'] == 'view_dataset':
    #     popup("Opening an external link ⚠️", [
    #         put_text('This website would like to open the external link below. Please click '
    #                  'the hyperlink below if you wish to continue, if not you may close this popup window.'),
    #         put_html('<a href="https://upsystem-my.sharepoint.com/:p:/g/personal/macabanlit_outlook_up_edu_ph/ETA9kG12UjFDkuo7jz1OP9UB6uik9EPSgclsGFR9TF19rg">View Presentation 📊</a>'),
    #         put_text(' '),
    #         put_buttons(['Close'], onclick=lambda _: close_popup())
    #     ])
    #
    # elif user_actions['action'] == 'browse_code':
    #     popup("Opening an external link ⚠️", [
    #         put_text('The heart disease prediction app would like to open the external link below. Please click '
    #                  'the hyperlink below if you wish to continue, if not you may close this popup window.'),
    #         put_html('<a href="https://github.com/mcabanlit/drug-store-chain">Visit GitHub 🗂️</a>'),
    #         put_text(' '),
    #         put_buttons(['Close'], onclick=lambda _: close_popup())
    #     ])

    # welcome()


app.add_url_rule('/', 'webio_view', webio_view(welcome),
                 methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    app.run()

# References:
# https://www.youtube.com/watch?v=jZB6OaHvPEQ
