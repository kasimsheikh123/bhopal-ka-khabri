
from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import pickle
import sklearn
locations = None
data_columns = None
model = None


def load_saved_arfifacts():
    print("LOADING saved artifacts.........>>>>>")
    global data_columns
    global locations

    with open("static/bhopal_colums.json", "r") as f:
        data_columns = json.load(f)["data_columns"]
        locations = data_columns[11:]

    global model
    with open("static/fixedbpl.pickle", "rb") as f:
        model = pickle.load(f)
    print("Loading Artifacts Donee....>>>")


def get_location():
    return locations


def get_data_columns():
    return data_columns


def get_estimated_price(sqft, bath, bhk, avail, furnish, trans, location):
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1
    avail_index = data_columns.index(avail)

    furnish_index = data_columns.index(furnish)

    trans_index = data_columns.index(trans)

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    if avail_index >= 0:
        x[avail_index] = 1
    if furnish_index >= 0:
        x[furnish_index] = 1
    if trans_index >= 0:
        x[trans_index] = 1
    return round(model.predict([x])[0], 2)


app = Flask(__name__, static_url_path="/static")


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route('/get_location_name', methods=['GET'])
def get_location_name():
    response = jsonify({
        'locations': get_location()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST', 'GET'])
def predict_home_price():
    avil = request.form['avail']
    fur = request.form['furnish']
    tran = request.form['trans']
    bat = int(request.form['bath'])
    bhk = int(request.form['bedroom'])
    tosqft = float(request.form['sqft'])
    locat = request.form['loc']
    response = jsonify({
        'estimated_price': get_estimated_price(tosqft, bat, bhk, avil, fur, tran, locat)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    print("Starting python Flask Server For Bhopal House Price Prediction")
    load_saved_arfifacts()
    app.run()