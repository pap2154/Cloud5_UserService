from flask import Flask, Response, request, render_template
#import database_services.RDBService as d_service
from flask_cors import CORS
import json

from application_services.imdb_artists_resource import IMDBArtistResource
from database_services.RDBService import RDBService as d_service
from application_services.user_resource import userResource as u_service
from application_services.address_resource import addressResource as a_service

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

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        res = u_service.get_all_users()
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp
    else:
        try:
            body = request.get_json()
            res = u_service.add_user(body)
            rsp = Response("Created!", status=201, content_type='application/json')
            return rsp
        except:
            rsp = Response("Error on POST", status=400, content_type='text/plain')
            return rsp

@app.route('/users/<userID>', methods=['GET','PUT', 'DELETE'])
def get_users_by_id(userID):
    if request.method == 'GET':
        res = u_service.get_user_by_id(userID)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp
    elif request.method == 'PUT':
        try:
            body = request.get_json()
            res = u_service.update_user(userID, body)
            rsp = Response("Updated!", status=201, content_type='application/json')
            return rsp
        except Exception as e:
            print(str(e))
            rsp = Response("Error on PUT", status=400, content_type='text/plain')
            return rsp
    else:
        try:
            res = u_service.delete_user(userID)
            rsp = Response("Deleted!", status=201, content_type='application/json')
            return rsp
        except Exception as e:
            print(str(e))
            rsp = Response("Error on DELETE", status=404, content_type='text/plain')
            return rsp


@app.route('/users/<userID>/address', methods=['GET'])
def get_address_by_user(userID):
    res = u_service.get_address_by_user("user_service", "user", "address", userID)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/addresses', methods=['GET', 'POST'])
def get_addresses():
    if request.method == 'GET':
        res = a_service.get_all_addresses()
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp
    else:
        try:
            body = request.get_json()
            res = a_service.add_address(body)
            rsp = Response("Created!", status=201, content_type='application/json')
            return rsp
        except:
            rsp = Response("Error on POST", status=400, content_type='text/plain')
            return rsp

@app.route('/addresses/<addressID>', methods=['GET','PUT', 'DELETE'])
def get_addresses_by_id(addressID):
    if request.method == 'GET':
        res = a_service.get_address_by_id(addressID)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
        return rsp
    elif request.method == 'PUT':
        try:
            body = request.get_json()
            res = a_service.update_address(addressID, body)
            rsp = Response("Updated!", status=201, content_type='application/json')
            return rsp
        except Exception as e:
            print(str(e))
            rsp = Response("Error on PUT", status=400, content_type='text/plain')
            return rsp
    else:
        try:
            res = a_service.delete_address(addressID)
            rsp = Response("Deleted!", status=201, content_type='application/json')
            return rsp
        except Exception as e:
            print(str(e))
            rsp = Response("Error on DELETE", status=404, content_type='text/plain')
            return rsp

@app.route('/addresses/<addressID>/users', methods=['GET'])
def get_users_by_address(addressID):
    res = a_service.get_user_by_address(addressID)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0")
