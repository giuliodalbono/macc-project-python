from sqlalchemy import desc

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
            return jsonify({"error": "Invalid input: 'name', 'is_public' and 'user_id' are required"}), 400

        new_chat = chat.Chat(name=data['name'], is_public=data['is_public'], user_id=data['user_id'])

        db.db.session.add(new_chat)
        db.db.session.commit()

        return json.dumps(new_chat.to_dict(), indent=4), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_route.route('/<chat_id>', methods=['PUT'])
def change_privacy_policy(chat_id):
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        chat_to_update = (chat.Chat.query
                          .filter(chat.Chat.id == chat_id)
                          .first())

        if not chat_to_update:
            return jsonify({"error": "Chat not found"}), 404

        chat_to_update.is_public = not chat_to_update.is_public

        db.db.session.commit()

        return json.dumps(chat_to_update.to_dict(), indent=4), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_route.route('/<chat_id>', methods=['GET'])
def fetch_chat(chat_id):
    last_chat = (chat.Chat.query
                 .filter(chat.Chat.id == chat_id)
                 .first())
    return jsonify(last_chat.to_dict()), 200


@chat_route.route('/last-from-user/<user_id>', methods=['GET'])
def fetch_last_chat(user_id):
    last_chat = (chat.Chat.query
                 .filter(chat.Chat.user_id == user_id)
                 .order_by(desc(chat.Chat.last_update))
                 .first())
    return jsonify(last_chat.to_dict()), 200


@chat_route.route('/from-user/<user_id>', methods=['GET'])
def fetch_chats(user_id):
    chats = chat.Chat.query.filter(chat.Chat.user_id == user_id).all()
    return jsonify([u.to_dict() for u in chats]), 200
