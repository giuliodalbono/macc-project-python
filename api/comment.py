from db import db
from flask import Blueprint, jsonify, request
from model import comment
from validation import rest_validation
import json


comment_route = Blueprint('comment', __name__)


@comment_route.route('', methods=['POST'])
def add_comment():
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        data = request.get_json()

        if not rest_validation.validate_comment(data):
            return jsonify({"error": "Invalid input: 'message', 'user_id' and 'chat_id' are required"}), 400

        new_comment = comment.Comment(message=data['message'], user_id=data['user_id'], chat_id=data['chat_id'])

        db.db.session.add(new_comment)
        db.db.session.commit()

        return json.dumps(new_comment.to_dict(), indent=4), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@comment_route.route('/<chat_id>', methods=['GET'])
def fetch_comments(chat_id):
    comments = comment.Comment.query.filter(comment.Comment.chat_id == chat_id).all()
    return jsonify([u.to_dict() for u in comments])
