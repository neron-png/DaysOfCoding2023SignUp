from wsgiref.headers import Headers
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import sqlite3


ACTIVE_DAYS = [1, 2, 3, 4, 5]

app = Flask(__name__)
CORS(app)
ip = "localhost"
DATABASE = 'reviews.db'
connection = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = connection.cursor()

# @app.route("/", methods=["GET"])
# def search():

#     reviews = cursor.execute("""
#     SELECT review
#     FROM reviews
#     """)
    
#     review_comments = []
#     for review in reviews:
#         review_comments.append(review[0])

#     return Response(status=200)


@app.route("/activeDays", methods=["GET"])
def activeDays():

    activeDays = {
        "activeDays" : [x for x in ACTIVE_DAYS]
    }

    resp =  Response(response=json.dumps(activeDays), status=200, mimetype='application/json', headers={'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'})
    # resp.headers["Access-Control-Allow-Origin", "*"]
    return resp

@app.route("/createTeam", methods=["POST"])
def createTeam():
    resp = Response(json.dumps({"code": "abcde"}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp

@app.route("/joinTeam", methods=["POST"])
def joinTeam():
    resp = Response(json.dumps({"team": "MyChemicalBromance"}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp

@app.route("/participateSolo", methods=["POST"])
def participateSolo():
    resp = Response(json.dumps({"solo": "MyChemicalBromance"}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp

@app.route("/findTeam", methods=["POST"])
def findTeam():
    resp = Response(json.dumps({"solo": "MyChemicalBromance"}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp

app.run(host=ip, port=5000, debug=True)