import os
# import cv2
from flask import Flask, request, jsonify, make_response, send_file
import mysql.connector
import mysql
import bcrypt

import base64

import uuid

UPLOAD_DIRECTORY = "uploads"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ARGUS"
)

app = Flask(__name__)


@app.route("/")
def index():
    return send_file("index.html")

# region[ Events ]


@app.post("/login")
def login():
    email = request.form["email"]
    password = request.form["password"]

    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

    user = cursor.fetchone()
    cursor.close()

    if user == None:
        response = make_response()
        response.status_code = 403
        response.set_data("EMAIL OR PASSWORD INVALID")
        response.close()
        return response
    else:
        (id, name, email, hashed) = user

        if (bcrypt.checkpw(str(password).encode(), str(hashed).encode())):
            return jsonify({
                "id": id,
                "username": name,
                "email": email,
            })
        else:
            response = make_response()
            response.status_code = 403
            response.set_data("EMAIL OR PASSWORD INVALID")
            response.close()
            return response
# endregion

# region [Events]


@app.post("/register")
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = str(request.form["password"])

    hashed_password = bcrypt.hashpw(
        str(password).encode(), bcrypt.gensalt()).decode()

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users(name,email,password) VALUES (%s,%s,%s) ",
                       (username, email, hashed_password,))

        userId = cursor.lastrowid

        user = {
            "id": userId,
            "username": username,
            "email": email
        }

        db.commit()
        cursor.close()

        response = jsonify(user)
        response.status_code = 200
        response.close()

        return response
    except:
        response = make_response()
        response.status_code = 500
        response.set_data("ERROR CREATING USER")
        response.close()
        return response
# endregion

# region


@app.get("/uploads/<name>")
def getImage(name: str):
    print(f"{UPLOAD_DIRECTORY}/{name}")
    if (os.path.exists(f"{UPLOAD_DIRECTORY}/{name}")):
        return send_file(f"{UPLOAD_DIRECTORY}/{name}")
    else:
        return "File not found", 404
# endregion


@app.get("/trash/<id>")
def getTrash(id: int):
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT report_id, lat, lng, file_path FROM reports WHERE report_id = %s LIMIT 1", (id, ))

    report = cursor.fetchone()

    if (report is not None):
        return jsonify(report)
    else:
        return "Report not found", 404


@app.get("/trash/all")
def getAll():
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT report_id, lat, lng, file_path FROM reports;")
    reports = cursor.fetchall()
    if(len(reports) == 0):
        return [], 404
    
    return reports, 200


@app.route('/submit', methods=['POST'])
def submit():
    print(request.content_encoding)
    open("dumo.out", "w").write(str(request.form))

    id = request.form['id']
    lat = request.form["lat"]
    lng = request.form["lng"]

    filePath = f"{UPLOAD_DIRECTORY}/{str(uuid.uuid4())}.png"

    # Check if the request contains a file
    if request.form.get("image") == None:
        return 'No file uploaded', 400

    try:
        # Get the file from the request
        image_file = base64.b64decode(request.form.get('image'))

        # Save the image data to a file on disk
        open(filePath, "wb").write(image_file)

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO reports(lat, lng, file_path, user_id) VALUES (%s, %s, %s, %s)", (lat, lng, filePath,  id, ))

        uploadId = cursor.lastrowid

        cursor.close()
        db.commit()

        res = jsonify({
            "status": "OK",
            "message": "Report uploaded successfully"
        })
        res.status_code = 200
        res.close()

        return res
    except Exception as e:
        print(e)
        res = jsonify({
            "status": "FAIL",
            "message": f"Error while trying to upload report: {e}"
        })
        res.status_code = 500
        res.close()
        return res


app.run(host="0.0.0.0", port=5000)
