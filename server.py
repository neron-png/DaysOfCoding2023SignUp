from wsgiref.headers import Headers
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import sqlite3
import random
import re
import requests

##############
#   CONFIG   #
##############

ACTIVE_DAYS = [1, 2, 3, 4, 5]

app = Flask(__name__)
CORS(app)
ip = "localhost"
DATABASE = 'teams.db'
connection = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = connection.cursor()

#check if table already exists
cursor.execute('''CREATE TABLE IF NOT EXISTS teams
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             code TEXT NOT NULL,
             teamName TEXT NOT NULL,
             players INTEGER DEFAULT 0 NOT NULL,
             P1 TEXT,
             P2 TEXT,
             P3 TEXT,
             P4 TEXT
             )''')

connection.commit()


#############
#   CODE    #
#############

def checkDiscord(username):
    return bool(re.match(r".+#[0-9]{4}$", username))

def generateCode():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))

def sendWebhook(webhook_text):
    webhook_url = "https://discord.com/api/webhooks/964272870035423303/EXHDCtPXDsTJIxLooyqLGkfgA39aztCxihXs_Z9vcI2hxr1m2D9RPyaArRgm5kDKBjTm"
    message = {"content": webhook_text}
    response = requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})


@app.route("/activeDays", methods=["GET"])
def activeDays():

    activeDays = {
        "activeDays" : [x for x in ACTIVE_DAYS]
    }

    resp =  Response(response=json.dumps(activeDays), status=200, mimetype='application/json', headers={'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'})
    # resp.headers["Access-Control-Allow-Origin", "*"]
    return resp

####################
#   Create Team    #
####################
@app.route("/createTeam", methods=["POST"])
def createTeam():

    # Getting JSON data as a python DICT
    data = request.get_json()   
    team_name = data["team_name"].lower()
    discord_username = data["discord_username"]

    # Check data validity
    errorFlag = False
    errorText = ""
    if not team_name.isalnum():
        errorText = "Team name must be Alphanumeric, without spaces"
        errorFlag = True
    if len(team_name) > 32:
        errorText = "Team name may not exceed 32 characters"
        errorFlag = True
    if not checkDiscord(discord_username):
        errorText = "Invalid discord username. Example of a valid username: Jon Doe#7520"
        errorFlag = True
    
    if errorFlag:
        return Response(json.dumps({"error": errorText}), status=418, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    
    # Generate team code
    code = generateCode()

    # Check if a team with that name exists already
    exists_check = cursor.execute("""
    SELECT EXISTS(
        SELECT 1
        FROM teams
        where teamName = ?
        )
    """, (team_name, )) # Note the trailing comma, it's intentional to convert to tuple
    
    # If they don't exist, create a new entry into the database
    if exists_check.fetchone() == (0,):

        # Add team to database
        cursor.execute("""
        INSERT INTO teams (code, players, teamName, P1)
        VALUES(?, ?, ?, ?)
        """, (code, 1, team_name, discord_username))
        connection.commit()

        # Success message
        resp = Response(json.dumps({"code": code}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})

        # Fallback message to the discord server
        sendWebhook(f"{discord_username} **created** {team_name} **with code** {code}")

    else:
        resp = Response(json.dumps({"error": "Υπάρχει ήδη ομάδα με αυτό το όνομα!"}), status=418, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})

    return resp


##################
#   Join Team    #
##################
@app.route("/joinTeam", methods=["POST"])
def joinTeam():

    # Getting JSON data as a python DICT
    data = request.get_json()   
    code = data["invitecode"].upper()
    discord_username = data["discord_username"]

    # Checking data validity
    errorFlag = False
    errorText = ""
    # Check if a team with that code exists
    exists_check = cursor.execute("""
    SELECT EXISTS(
        SELECT 1
        FROM teams
        where code = ?
        )
    """, (code, )) # Note the trailing comma, it's intentional to convert to tuple

    if exists_check.fetchone == (0,):
        errorFlag = True
        errorText = "Δεν υπάρχει ομάδα με αυτόν τον κωδικό. Εάν πιστεύετε ότι αυτό είναι λάθος, στείλτε μας ένα μήνυμα στο discord server της εκδήλωσης https://discord.com/invite/uzs9JHqFAP"
    if not checkDiscord(discord_username):
        errorText = "Invalid discord username. Example of a valid username: Jon Doe#7520"
        errorFlag = True
    
    # check if team is full
    teamRow = cursor.execute("""select * from teams where code = ?""", (code,)).fetchone()
    teamMembers = teamRow[3]
    if teamMembers == 4:
        errorFlag = True
        errorText = "Αυτή η ομάδα είναι ήδη πλήρης! Εάν πιστεύετε ότι αυτό είναι λάθος, στείλτε μας ένα μήνυμα στο discord server της εκδήλωσης https://discord.com/invite/uzs9JHqFAP"
    
    if errorFlag:
        return Response(json.dumps({"error": errorText}), status=418, mimetype='application/json',
                        headers={   'Access-Control-Allow-Origin': '*',
                                    'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})

    # No problems with the data, let's add the user!
    PID = f"P{teamMembers+1}"
    cursor.execute(f"""UPDATE teams SET {PID} = ? WHERE code = ?""", (discord_username, code,))
    cursor.execute(f"""UPDATE teams SET players = ? WHERE code = ?""", (teamMembers+1, code,))
    connection.commit()

    # Backup message to discord
    sendWebhook(f"{discord_username} **joined** {teamRow[2]} **with code** {code} [{teamRow[3]+1}/4]")


    resp = Response(json.dumps({"team": teamRow[2]}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp


#################
#   Solo Team   #
#################
@app.route("/participateSolo", methods=["POST"])
def participateSolo():
    resp = Response(json.dumps({"solo": "MyChemicalBromance"}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp


#################
#   Find Team   #
#################
@app.route("/findTeam", methods=["POST"])
def findTeam():
    resp = Response(json.dumps({"solo": "MyChemicalBromance"}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp

app.run(host=ip, port=5000, debug=True)