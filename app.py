import json
import os

from flask import Flask, request, render_template, redirect, url_for, Response, Blueprint

from site_cls import Site
from workspaces import Workspace, Storage

if os.path.exists('/SERVER/is_server') or True:
    prefix = '/web-workspaces'
else:
    prefix = '/'

appbp = Blueprint('app', __name__, url_prefix=prefix)

storage = Storage('workspaces.json')
storage.load()


@appbp.route('/')
def start():
    return render_template('start.html')


@appbp.route('/<code>')
def workspace(code):
    sites = storage.get_or_create_workspace(code).sites
    return render_template('workspace.html', code=code, sites=sites)


def workspace_indexed_action(func, code, index):
    wsp = storage.get_or_null(code)
    if wsp and index.isdigit():
        func(wsp, index)
        storage.save()
        return '', 200
    return '', 400


@appbp.route('/<code>/add-site')
def add_site(code):
    url = request.args.get('url', '')
    name = request.args.get('name', '')

    if url and name:
        storage.get_or_create_workspace(code).add(Site(name, url))
        storage.save()

        return '', 200
    return '', 400


@appbp.route('/<code>/remove-site-at')
def remove_site(code):
    return workspace_indexed_action(
        lambda wsp, idx: wsp.remove_at(idx),
        code,
        request.args.get('index', '')
    )


@appbp.route('/<code>/move-site-down')
def move_site_down(code):
    return workspace_indexed_action(
        lambda wsp, idx: wsp.move_down(idx),
        code,
        request.args.get('index', '')
    )

@appbp.route('/<code>/move-site-up')
def move_site_up(code):
    return workspace_indexed_action(
        lambda wsp, idx: wsp.move_up(idx),
        code,
        request.args.get('index', '')
    )

app = Flask(__name__)
app.register_blueprint(appbp)


if __name__ == '__main__':
    app.run(debug=True)