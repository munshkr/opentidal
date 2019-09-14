import json

from bottle import request, response, route

from opentidal import __version__
from opentidal.predictor import predict
from opentidal.dataset import Dataset


@route('/')
def index():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'version': __version__})


@route('/submit', method='POST')
def submit():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': 'ok'})


@route('/generate')
def generate():
    output = sample_output()
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'output': output})