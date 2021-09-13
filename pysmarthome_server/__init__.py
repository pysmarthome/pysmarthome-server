from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, g, request, jsonify
from .middlewares import register_middlewares
from pysmarthome import PluginManager
from .db import db
from .config import config
from .graphql import mkschema
from .watchdog.watcher import reset_on_package_updates
from multiprocessing import Process

app = Flask(__name__)
app.config['API_KEY'] = config['api_key']
register_middlewares(app)
conn = db.init(config['db'])
server_options = { 'host': config['host'], 'port': config['port'] }
app_process = Process(target=app.run, kwargs=server_options)
reset_on_package_updates(app_process)
dev_controllers = PluginManager.init(conn)
schema = mkschema([ctrl.model_class for ctrl in dev_controllers.values()])
start_server = app_process.start


@app.route('/graphql', methods=['GET'])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route('/graphql', methods=['POST'])
def graphql():
    success, result = graphql_sync(
        schema,
        request.get_json(),
        context_value={
            'request': request,
            'g': g,
        },
        debug=True
    )
    return jsonify(result), 200 if success else 400


@app.before_request
def before_request():
    g.plugin_manager = PluginManager

@app.teardown_request
def teardown_request(exception):
    g.pop('plugin_manager', None)
