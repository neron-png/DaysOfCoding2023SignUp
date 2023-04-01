from wsgiref.headers import Headers
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import sqlite3
import random
import re
import requests
from problems import day0,day1,day2,day3,day4,day5,day6,day7

##############
#   CONFIG   #
##############

ACTIVE_DAY = 2

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


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    
    lb = {"leaderboard": [{"team": "Test team 1",
                        "id": "team_code",
                        "score": "666",
                        "members": "Neron"},
     {"team": "team_name",
                        "id": "team_code",
                        "score": "score",
                        "members": "member"}],
     "updated": "2022-03-31 21:02"
     }
    
    with open("leaderboard.json", "r") as f:
        lb = json.load(f)
    
    
    resp = Response(response=json.dumps(lb), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    # resp.headers["Access-Control-Allow-Origin", "*"]
    return resp


@app.route("/problem_checking", methods=["POST"])
def problem_checking():

    global ACTIVE_DAY
    
    try:
        with open("activeDay", 'r+') as f:
            ACTIVE_DAY = int(f.readline())
    except Exception as e:
        print(e)
        pass
    
    data = request.get_json()
    test_case = data["test_case"]
    result = ""

    problem_activations = {
        0: day0.run,
        1: day1.run,
        2: day2,
        3: day3,
        4: day4,
        5: day5,
        6: day6,
        7: day7.run
    }
    if ACTIVE_DAY == 0:
        result = problem_activations[0](test_case=test_case)
    
    if ACTIVE_DAY == 1:
        result = problem_activations[1](test_case)
    
    if ACTIVE_DAY == 2:
        result = day2.Basketball().run(test_case=test_case)

    if ACTIVE_DAY == 7:
        result = day7.run(test_case)

    # result = problem_activations[ACTIVE_DAY](test_case)
    print(ACTIVE_DAY)
    print(result)


    resp = Response(response=json.dumps({"result": result}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    # resp.headers["Access-Control-Allow-Origin", "*"]
    return resp


@app.route("/activeDay", methods=["GET"])
def activeDay():

    global ACTIVE_DAY

    try:
        with open("activeDay", 'r+') as f:
            ACTIVE_DAY = int(f.readline())
    except Exception as e:
        print(e)
        pass

    activeDay = {
        "activeDay" : ACTIVE_DAY
    }

    resp =  Response(response=json.dumps(activeDay), status=200, mimetype='application/json', headers={'Access-Control-Allow-Origin':'*',
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
    full_name = data["full_name"]

    # Check data validity
    errorFlag = False
    errorText = ""
    if not team_name.isalnum():
        errorText = "Το όνομα της ομάδας πρέπει να είναι αλφανουμερικό χωρίς κενά!"
        errorFlag = True
    if len(team_name) > 32:
        errorText = "Το όνομα της ομάδας δεν μπορεί να ξεπερνάει τους 32 χαρακτήρες!"
        errorFlag = True
    if not checkDiscord(discord_username):
        errorText = "Εσφαλμένο discord username. Παράδειγμα αποδεκτού username: Jon Doe#7520"
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
        sendWebhook(f"{full_name} with discord username {discord_username} **created** {team_name} **with code** {code}")

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
    full_name = data["full_name"]

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
        errorText = "Εσφαλμένο discord username. Παράδειγμα αποδεκτού username: Jon Doe#7520"
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
    sendWebhook(f"{full_name} with discord username {discord_username} **joined** {teamRow[2]} **with code** {code} [{teamRow[3]+1}/4]")


    resp = Response(json.dumps({"team": teamRow[2]}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp


#################
#   Solo Team   #
#################
@app.route("/participateSolo", methods=["POST"])
def participateSolo():

    # Getting JSON data as a python DICT
    data = request.get_json()
    discord_username = data["discord_username"]
    full_name = data["full_name"]

    # Checking data validity
    errorFlag = False
    errorText = ""
    if not checkDiscord(discord_username):
        errorText = "Εσφαλμένο discord username. Παράδειγμα αποδεκτού username: Jon Doe#7520"
        errorFlag = True
    if errorFlag:
        return Response(json.dumps({"error": errorText}), status=418, mimetype='application/json',
                        headers={   'Access-Control-Allow-Origin': '*',
                                    'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    
    # Adding the user to the DB as a solo participation
    code = generateCode()
    cursor.execute("""
        INSERT INTO teams (code, players, teamName, P1)
        VALUES(?, ?, ?, ?)
        """, (code, 666, discord_username, discord_username))
    connection.commit()

    # Backup message to discord
    sendWebhook(f"{full_name} with discord username {discord_username} **joined Solo** **with code** {code}")

    resp = Response(json.dumps({"": ""}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp


#################
#   Find Team   #
#################
@app.route("/findTeam", methods=["POST"])
def findTeam():
    
    # Getting JSON data as a python DICT
    data = request.get_json()
    discord_username = data["discord_username"]
    full_name = data["full_name"]

    # Checking data validity
    errorFlag = False
    errorText = ""
    if not checkDiscord(discord_username):
        errorText = "Εσφαλμένο discord username. Παράδειγμα αποδεκτού username: Jon Doe#7520"
        errorFlag = True
    if errorFlag:
        return Response(json.dumps({"error": errorText}), status=418, mimetype='application/json',
                        headers={   'Access-Control-Allow-Origin': '*',
                                    'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    
    # Adding the user to the DB as a solo participation
    code = generateCode()
    cursor.execute("""
        INSERT INTO teams (code, players, teamName, P1)
        VALUES(?, ?, ?, ?)
        """, (code, 555, discord_username, discord_username))
    connection.commit()

    # Backup message to discord
    sendWebhook(f"{full_name} with discord username {discord_username} **joined and is looking for a team!** **with code** {code}")

    resp = Response(json.dumps({"": ""}), status=200, mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Methods': 'POST,PATCH,OPTIONS'})
    return resp

app.run(host=ip, port=5000, debug=True)
