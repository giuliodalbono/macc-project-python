from db import config
from model import user
from validation import rest_validation
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import git

app = Flask(__name__)

app.config.from_object(config.Config)

db = SQLAlchemy(app)


@app.route('/git-update', methods=['POST'])
def git_update():
    repo = git.Repo("./macc-project-python")
    origin = repo.remotes.origin
    repo.create_head("main", origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return "", 200


@app.route('/')
def hello_world():
    return 'Final test, githook works!'


@app.route('/add-user', methods=['POST'])
def add_user():
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        json = request.get_json()

        if not rest_validation.validate_user(json):
            return jsonify({"error": "Invalid input, 'uid', 'email' and username are required"}), 400

        new_user = user.User(uid=json['uid'], email=json['email'], username=json['username'])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User added successfully!", "user": new_user.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fetch-users')
def fetch_users():
    users = user.User.query.all()
    return jsonify([u.to_dict() for u in users])


if __name__ == '__main__':
    app.run()
