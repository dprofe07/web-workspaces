import json
import os

from flask import Flask, request, render_template, redirect, url_for, Response, Blueprint

if os.path.exists('/SERVER/is_server') or True:
    prefix = '/web-workspaces'
else:
    prefix = '/'

appbp = Blueprint('app', __name__, url_prefix=prefix)
DATA_FILE = 'workspaces.json'

workspaces = {}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

with open(DATA_FILE, 'r') as f:
    workspaces = json.load(f)



def save_workspaces(workspaces):
    with open(DATA_FILE, 'w') as f:
        json.dump(workspaces, f)


@appbp.route('/')
def start():
    return render_template('start.html')


@appbp.route('/<code>')
def workspace(code):
    sites = workspaces.get(code, [])
    return render_template('index.html', code=code, sites=sites)


@appbp.route('/<code>/add-site')
def add_site(code):
    url = request.args.get('url', '')
    name = request.args.get('name', '')

    if url and name:
        if code not in workspaces:
            workspaces[code] = []

        workspaces[code].append({'name': name, 'url': url})
        save_workspaces(workspaces)

    return '', 200


@appbp.route('/<code>/remove-site-at')
def remove_site(code):
    index = request.args.get('index', '')

    if index.isdigit():
        index = int(index)

        if code in workspaces and 0 <= index < len(workspaces[code]):
            workspaces[code].pop(index)
            save_workspaces(workspaces)

    return '', 200

app = Flask(__name__)
app.register_blueprint(appbp)


if __name__ == '__main__':
    app.run(debug=True)