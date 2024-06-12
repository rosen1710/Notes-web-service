from flask import Flask, request, make_response #, jsonify
from flask_cors import CORS
import requests
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
# import sqlalchemy.exc

from models import *

db_host = "localhost" # "db-loadbalancer"

keycloak_host = "localhost" # "keycloak"
realm_id = "notes-web-service"
client_id = "notes-web-service-backend"
client_secret = "QXLSo3kG8ZRa64G1UJ7wZSqViefTqMW7"

app = Flask(__name__)
CORS(app)

def create_db_engine():
    return create_engine(f"mariadb+pymysql://rosen:announcements_service@{db_host}:3306/notes_db")

@app.route("/", methods=["GET", "POST"])
def validate_token():
    data = request.json
    response = requests.post(f"http://{keycloak_host}:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": data["token"]}).json()
    return make_response(response, 200)

@app.route("/note/all", methods=["GET"])
def get_all_notes():
    engine = create_db_engine()

    with Session(engine) as session:
        notes = session.scalars(select(Note))

        result = []
        for note in notes:
            result.append({})
            result[-1]["id"] = note.id
            result[-1]["user_id"] = note.user_id
            result[-1]["title"] = note.title
            result[-1]["description"] = note.description
            result[-1]["date_time"] = note.date_time

        session.commit()

    return make_response({
        "message": "Notes was fetched successfully",
        "notes": result
    }, 200)

@app.route("/note", methods=["POST"])
def add_note():
    data = request.json

    response = requests.post(f"http://{keycloak_host}:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": data["token"]}).json()

    if response["active"] == False:
        return make_response({"message": "Unauthorized"}, 401)

    engine = create_db_engine()

    with Session(engine) as session:
        session.add(
            Note(
                user_id=response["sub"],
                title=data["title"],
                description=data["description"]
            )
        )
        session.commit()

    return make_response({"message": "Note was added successfully"}, 200)

@app.route("/note/<int:note_id>", methods=["PUT"])
def edit_note(note_id):
    data = request.json

    response = requests.post(f"http://{keycloak_host}:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": data["token"]}).json()

    if response["active"] == False:
        return make_response({"message": "Unauthorized"}, 401)

    engine = create_db_engine()

    with Session(engine) as session:
        note = session.scalar(select(Note).where(Note.id == note_id))

        if note is None:
            return make_response({"message": "Note not found"}, 404)
        if note.user_id != response["sub"]:
            return make_response({"message": "Note not found"}, 404)

        note.title = data["title"]
        note.description = data["description"]

        session.commit()

    return make_response({"message": "Note was edited successfully"}, 200)

@app.route("/note/<int:note_id>/<string:token>", methods=["DELETE"])
def delete_note(note_id, token):
    response = requests.post(f"http://{keycloak_host}:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": token}).json()

    if response["active"] == False:
        return make_response({"message": "Unauthorized"}, 401)

    engine = create_db_engine()

    with Session(engine) as session:
        note = session.scalar(select(Note).where(Note.id == note_id))

        if note is None:
            return make_response({"message": "Note not found"}, 404)
        if note.user_id != response["sub"]:
            return make_response({"message": "Note not found"}, 404)

        session.delete(note)

        session.commit()

    return make_response({"message": "Note was deleted successfully"}, 200)

# Base.metadata.create_all(create_db_engine())

if __name__ == "__main__":
    app.run(port=5002, host="0.0.0.0", debug=True)