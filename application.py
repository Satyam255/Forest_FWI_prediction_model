import pickle
from flask import Flask,request,jsonify,render_template
import numpy as numpy
import pandas as pd
from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
app = application


## import ridge regression model and standard scaler pickle files
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['POST', 'GET'])
def predict_datapoint():
    if request.method == 'POST':
        Temperature = float(request.form['temp'])
        RH = float(request.form['rh'])
        WS = float(request.form['ws'])
        Rain = float(request.form['rain'])
        FFMC = float(request.form['ffmc'])
        DMC = float(request.form['dmc'])
        ISI = float(request.form['isi'])
        Classes = float(request.form['classes'])
        Region = float(request.form['Region'])

        new_data_scaled = standard_scaler.transform(
            [[Temperature, RH, WS, Rain, FFMC, DMC, ISI, Classes, Region]]
        )
        result = ridge_model.predict(new_data_scaled)

        # Corrected: send the prediction under the correct variable name
        return render_template('index.html', prediction='{:.2f}'.format(result[0]))
    else:
        return render_template('index.html')




if __name__ == "__main__":
    app.run(host="0.0.0.0")