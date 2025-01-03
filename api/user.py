from app import app
from db import db
from flask import jsonify, request
from model import user
from validation import rest_validation
import json


@app.route('/add-user', methods=['POST'])
def add_user():
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        data = request.get_json()

        if not rest_validation.validate_user(data):
            return jsonify({"error": "Invalid input: 'uid', 'email' and 'username' are required"}), 400

        new_user = user.User(uid=data['uid'], email=data['email'], username=data['username'])

        db.db.session.add(new_user)
        db.db.session.commit()

        return json.dumps(new_user.to_dict(), indent=4), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fetch-users')
def fetch_users():
    users = user.User.query.all()
    return jsonify([u.to_dict() for u in users])
