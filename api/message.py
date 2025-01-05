from db import db
from flask import Blueprint, jsonify, request
from model import message
from validation import rest_validation
import json


message_route = Blueprint('message', __name__)


@message_route.route('', methods=['POST'])
def add_message():
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        data = request.get_json()

        if not rest_validation.validate_message(data):
            return jsonify({"error": "Invalid input: 'message', 'translation', 'city' and 'chat_id' are required"}), 400

        new_message = message.Message(message=data['message'], translation=data['translation'], city=data['city'],
                                      chat_id=data['chat_id'])

        db.db.session.add(new_message)
        db.db.session.commit()

        return json.dumps(new_message.to_dict(), indent=4, default=str), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@message_route.route('/<chat_id>', methods=['GET'])
def fetch_messages(chat_id):
    messages = message.Message.query.filter(message.Message.chat_id == chat_id).all()
    return jsonify([u.to_dict() for u in messages])
