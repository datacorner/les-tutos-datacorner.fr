from flask import Flask
import pandas as pd
from sklearn import linear_model
from joblib import dump, load

app = Flask(__name__)

def fitgen():
    data = pd.read_csv("../datasources/univariate_linear_regression_dataset.csv")
    X = data.col2.values.reshape(-1, 1)
    y = data.col1.values.reshape(-1, 1)
    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    return regr

@app.route('/fit30/')
def fit30():
    regr = fitgen()
    return str(regr.predict([[30]]))

@app.route('/fit/<prediction>')
def fit(prediction):
    regr = fitgen()
    return str(regr.predict([[int(prediction)]]))

@app.route('/predict/<prediction>')
def predict(prediction):
    regr = load('monpremiermodele.modele')
    return str(regr.predict([[int(prediction)]]))

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=8080)