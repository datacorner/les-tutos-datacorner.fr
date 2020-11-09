from eve import Eve
from utils.operations import ajoute_deux

app = Eve()

@app.route('/hello')
def hello_world():
    return 'hello world!' + str(ajoute_deux(1))

if __name__ == '__main__':
    app.run()
