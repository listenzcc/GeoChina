import os
import pandas as pd
import json
from flask import Flask
from flask import Response
from setting import config

mimetypes = dict(
    pdf='application/pdf',
    json='application/json',
)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/<name>')
def index(name):
    if not name in os.listdir('.'):
        return f'Can not find {name}', 404

    resp = open(name, 'rb').read()
    if '.' in name:
        ext = name.split('.')[-1]
        if ext in mimetypes:
            resp = Response(resp, mimetype=mimetypes[ext])
    return resp


# @app.route('/main.json')
# def default():
#     path = os.path.join(config['Local']['dataFolder'], 'main.json')
#     with open(path, 'r') as fp:
#         obj = json.load(fp)
#     return obj


if __name__ == '__main__':
    app.run()
