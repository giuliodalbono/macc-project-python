from db import db
from flask import Blueprint, jsonify, request
from model import chat
from validation import rest_validation
import json


chat_route = Blueprint('chat', __name__)


@chat_route.route('', methods=['POST'])
def add_chat():
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        data = request.get_json()

        if not rest_validation.validate_chat(data):
            return jsonify({"error": "Invalid input: 'id', 'name', 'is_public' and 'user_id' are required"}), 400

        new_chat = chat.Chat(id=data['id'], name=data['name'], is_public=data['is_public'], user_id=data['user_id'])

        db.db.session.add(new_chat)
        db.db.session.commit()

        return json.dumps(new_chat.to_dict(), indent=4), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_route.route('', methods=['GET'])
def fetch_users():
    chats = chat.Chat.query.all()
    return jsonify([u.to_dict() for u in chats])
