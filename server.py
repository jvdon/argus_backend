import os
import cv2
from flask import Flask, request, jsonify, make_response
import mysql.connector
import bcrypt

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ARGUS"
)

app = Flask(__name__)


@app.post("/login")
def login():
    email = request.json["email"]
    password = request.json["password"]

    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

    user = cursor.fetchone()
    cursor.close()

    if user == None:
        response = make_response()
        response.status_code = 404
        response.set_data("USER NOT FOUND")
        response.close()
        return response
    else:
        (id, name, email, hashed) = user

        if (bcrypt.checkpw(str(password).encode(), str(hashed).encode())):
            return jsonify({
                "username": name,
                "email": email,
            })
        else:
            response = make_response()
            response.status_code = 403
            response.set_data("EMAIL OR PASSWORD INVALID")
            response.close()
            return response


@app.post("/register")
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = str(request.json["password"])

    hashed_password = bcrypt.hashpw(
        str(password).encode(), bcrypt.gensalt()).decode()

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users(name,email,password) VALUES (%s,%s,%s) ", (username, email, hashed_password,))
        db.commit()
        cursor.close()

        response = make_response()
        response.status_code = 200
        response.set_data("USER CREATED")
        response.close()

        return jsonify(request.json)
    except:
        response = make_response()
        response.status_code = 500
        response.set_data("ERROR CREATING USER")
        response.close()
        return response


app.run(host="0.0.0.0", port=5000)
