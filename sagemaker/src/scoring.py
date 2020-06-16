# This is the file that implements a flask server to do inferences.

from __future__ import print_function

import pandas as pd
import flask
import json
from json import encoder

from model_api import ModelHandler

encoder.FLOAT_REPR = lambda o: format(o, '.5f')


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this container, we declare
    it healthy if we can load the models successfully."""
    health = ModelHandler.health_check()

    if health:
        status = 200
    else:
        status = 404

    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def score():
    data = None
    result = {}

    if flask.request.content_type == 'application/json':
        data = flask.request.data.decode('utf-8')
    else:
        return flask.Response(response="This scoring model only supports json requests",
                              status=415, mimetype='application/json')
    req = json.loads(data)

    result = {
        'name': 'senator-nlp-vote-prediction',
        'score_data': ModelHandler.predict(req['summary'],
                                           req['sponsor_party'],
                                           int(req['num_co_D']),
                                           int(req['num_co_R']),
                                           int(req['num_co_ID']),
                                           pd.read_json(req['dataframe'])).to_json()
    }
    result_string = json.dumps(result)

    return flask.Response(response=result_string, status=200, mimetype='application/json')
