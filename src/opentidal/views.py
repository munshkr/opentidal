import json
import random

from bottle import get, post, redirect, request, response, static_file, view

from opentidal import __version__
from opentidal.model import (BATCH_SIZE, DEFAULT_DATASET_NAME,
                             DEFAULT_MODEL_PATH, SEQUENCE_LENGTH, DataProvider,
                             predict)


@get('/')
@view('index')
def index():
    data_provider = DataProvider(DEFAULT_DATASET_NAME, BATCH_SIZE,
                                 SEQUENCE_LENGTH)
    samples = data_provider.get_samples(5)
    predicted_samples = predict(DEFAULT_MODEL_PATH, num_samples=5)
    predicted_samples = [
        random.sample(sample.split("\n"), 1)[0].strip()
        for sample in predicted_samples
    ]
    return dict(version=__version__,
                samples=samples,
                predicted_samples=predicted_samples)


@get('/feed')
@view('feed')
def feed():
    return dict(version=__version__)


@post('/feed')
def feed_submit():
    code = request.forms.get("collab")
    # Extract line
    lines = code.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    code = lines[0]
    data_provider = DataProvider(DEFAULT_DATASET_NAME, BATCH_SIZE,
                                 SEQUENCE_LENGTH)
    data_provider.append(code)
    redirect("/")


@get('/growth')
@view('growth')
def growth():
    return dict(version=__version__)


@get('/resources')
@view('resources')
def resources():
    return dict(version=__version__)


@get('/api/?')
def api_index():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'version': __version__})


@post('/api/submit')
def api_submit():
    # FIXME should accept json
    response.headers['Content-Type'] = 'application/json'
    data_provider = DataProvider(DEFAULT_DATASET_NAME, BATCH_SIZE,
                                 SEQUENCE_LENGTH)
    data_provider.append(request.body)
    return json.dumps({'status': 'ok'})


@get('/api/generate')
def api_generate():
    response.headers['Content-Type'] = 'application/json'
    output = predict(MODEL_PATH, num_samples=1)
    return json.dumps({'output': output})


@get('/<filename:path>')
def get_static(filename):
    return static_file(filename, root='static')
