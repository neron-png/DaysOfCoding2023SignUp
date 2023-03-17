from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
ip = "localhost"
DATABASE = 'reviews.db'
connection = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = connection.cursor()

@app.route("/", methods=["GET"])
def search():

    reviews = cursor.execute("""
    SELECT review
    FROM reviews
    """)
    
    review_comments = []
    for review in reviews:
        review_comments.append(review[0])

    return Response(status=200)

app.run(host=ip, port=5000, debug=False)