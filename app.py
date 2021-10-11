from flask import Flask, Response, render_template
import database_services.RDBService as d_service
from flask_cors import CORS
import json

from application_services.imdb_artists_resource import IMDBArtistResource

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello Patis World!'
    # return render_template(static/simple-test.html)


@app.route('/imdb/artists/<prefix>')
def get_artists_by_prefix(prefix):
    res = IMDBArtistResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = d_service.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/users')
def get_users():
    res = d_service.get_resource("user_service", "user")
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/users/<userID>')
def get_users_by_id(userID):
    res = d_service.get_resource_by_id("user_service", "user", userID)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/users/<userID>/address')
def get_address_by_user(userID):
    res = d_service.get_resource_by_user("user_service", "user", "address", userID)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/addresses')
def get_addresses():
    res = d_service.get_resource("user_service", "address")
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/addresses/<addressID>')
def get_addresses_by_id(addressID):
    res = d_service.get_resource_by_id("user_service", "address", addressID)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/addresses/<addressID>/users')
def get_user_by_address(addressID):
    res = d_service.get_resource_by_user("user_service", "address", "user", addressID)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0")
