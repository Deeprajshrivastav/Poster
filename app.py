import pandas as pd
import numpy as np
import pickle
from flask import Flask, render_template, request, url_for, redirect

model = pickle.load(open('rain.pkl', 'rb'))
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    inputValue = []
    for i in request.form.values():
        inputValue.append(i)

    if len(inputValue) == 0:
        return redirect(url_for('predict'))

    feature = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation',
        'Sunshine', 'WindGustDir', 'WindGustSpeed','Temp9am', 'Cloud9am',
                'RainToday']



    inputValue = [np.array(inputValue)]


    w = ['W', 'NNW', 'SE', 'ENE', 'SW', 'SSE', 'S', 'NE','SSW', 'N', 'WSW', 'ESE', 'E', 'NW', 'WNW', 'NNE']
    ind = w.index(inputValue[0][5])


    wc = [13,  6,  9,  1, 12, 10,  8,  4, 11,  3, 15,  2,  0,  7, 14,  5]
    inputValue[0][5] = wc[ind]


    ry = inputValue[0][len(inputValue)-1]

    if ry.lower() == 'yes':
        inputValue[0][len(inputValue[0])-1] = 1
    else:
        inputValue[0][len(inputValue[0])-1] = 0

    data = pd.DataFrame(inputValue, columns=feature)

    try:
        x = model.predict(data)


    except Exception as e:
        print(e)
        return redirect(url_for('predict'))

    if x[0] == 0:
        result = "No Rain tomorrow"
    else:
        result = "rain tomorrow"
    return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
