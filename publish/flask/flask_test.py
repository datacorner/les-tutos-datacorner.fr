# sous ubuntu lancer d'abord $ apt-get install python3-flask
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello datacorner.fr !"

if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=8080)