import json

from bottle import get, post, request, response, static_file, view

from opentidal import __version__
from opentidal.dataset import Dataset
from opentidal.model import predict


@get('/')
@view('index')
def index():
    return dict(version=__version__)


@get('/feed')
@view('feed')
def index():
    return dict(version=__version__)


@get('/api')
def api_index():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'version': __version__})


@post('/api/submit')
def api_submit():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': 'ok'})


@get('/api/generate')
def api_generate():
    output = predict(MODEL_PATH)
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'output': output})


@get('/<filename:path>')
def get_static(filename):
    return static_file(filename, root='static')
