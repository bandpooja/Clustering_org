from flask import Flask, jsonify, make_response
from unsupervised_clustering.final_evaluation import *
import requests


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)


# sanity check route
@app.route('/prediction/<string:id>', methods=['GET'])
def make_prediction(id):
    print('request came in')
    print(id)
    url_path = f'http://on34c02847195.cihs.ad.gov.on.ca:8080/api/employee_group/{id}/names'
    response = requests.get(url_path)
    data = response.json()
    print(data)
    names =[]
    for org_name in data:
        names.append(org_name['Organization_name'])
    print(names)
    preds = make_group_predictions(names) 
    f = open("prediction.txt", "w")
    f.write({"predictions": preds})
    f.close()
    print("Predictions:",preds)
    return None


if __name__ == '__main__':
    app.run(port=8081)
