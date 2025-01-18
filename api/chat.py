from db import db
from flask import Blueprint, jsonify, request
from model import chat, user
from sqlalchemy import desc
from sqlalchemy.sql import text
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

        return json.dumps(new_chat.to_dict(), indent=4, default=str), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_route.route('/<chat_id>', methods=['PUT'])
def change_privacy_policy(chat_id):
    try:
        chat_to_update = (chat.Chat.query
                          .filter(chat.Chat.id == chat_id)
                          .first())

        if not chat_to_update:
            return jsonify({"error": "Chat not found"}), 404

        chat_to_update.is_public = not chat_to_update.is_public

        db.db.session.commit()

        return json.dumps(chat_to_update.to_dict(), indent=4, default=str), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_route.route('/<chat_id>', methods=['GET'])
def fetch_chat(chat_id):
    last_chat = (chat.Chat.query
                 .filter(chat.Chat.id == chat_id)
                 .first())
    return json.dumps(last_chat.to_dict(), indent=4, default=str), 200


@chat_route.route('/last-from-user/<user_id>', methods=['GET'])
def fetch_last_chat(user_id):
    last_chat = (chat.Chat.query
                 .filter(chat.Chat.user_id == user_id)
                 .order_by(desc(chat.Chat.last_update))
                 .first())

    query = """
        SELECT * FROM message m1
        JOIN message m2
        ON m1.chat_id = m2.chat_id
        AND m1.creation_time = m2.creation_time
        WHERE m2.chat_id = :chat_id
        GROUP BY m2.chat_id;
    """

    row = db.db.session.execute(text(query), {'chat_id': last_chat.id}).fetchone()
    if row:
        row_as_dict = row._asdict()

        last_chat = last_chat.to_dict()
        if row_as_dict["message"] is not None:
            last_chat['preview'] = row_as_dict["message"]
        return json.dumps(last_chat, indent=4, default=str), 200
    else:
        last_chat = last_chat.to_dict()
        return json.dumps(last_chat, indent=4, default=str), 200


@chat_route.route('/from-user/<user_id>', methods=['GET'])
def fetch_chats(user_id):
    chats = (chat.Chat.query
             .filter(chat.Chat.user_id == user_id)
             .order_by(desc(chat.Chat.creation_time))
             .all())

    ids = [c.id for c in chats]

    query = """
        SELECT * FROM message m1
        JOIN message m2
        ON m1.chat_id = m2.chat_id
        AND m1.creation_time = m2.creation_time
        WHERE m2.chat_id IN :ids
        GROUP BY m2.chat_id;
    """

    rows = db.db.session.execute(text(query), {"ids": tuple(ids)}).fetchall()
    rows_as_dicts = [r._asdict() for r in rows]

    chats_as_dict_list = []

    for c in chats:
        c = c.to_dict()
        c["preview"] = next((r["message"] for r in rows_as_dicts if r["chat_id"] == c["id"]), None)
        chats_as_dict_list.append(c)

    return json.dumps(chats_as_dict_list, indent=4, default=str), 200


@chat_route.route('/community', methods=['GET'])
def fetch_community_chats():
    try:
        # Fetch public chats with usernames of users who created them
        chats = (
            db.db.session.query(chat.Chat, user.User.username)
            .join(user.User, chat.Chat.user_id == user.User.uid)
            .filter(chat.Chat.is_public.is_(True))
            .order_by(desc(chat.Chat.last_update))
            .all()
        )

        # Extract chat IDs to fetch message previews
        ids = [c.Chat.id for c in chats]
        if not ids:
            return jsonify([]), 200  # Handle empty list of chats

        # Query messages to get the latest message preview for each chat
        query = """
            SELECT m1.id AS message_id, m1.chat_id, m1.message, m1.creation_time
            FROM message m1
            INNER JOIN (
                SELECT chat_id, MAX(creation_time) AS max_time
                FROM message
                WHERE chat_id IN :ids
                GROUP BY chat_id
            ) m2 ON m1.chat_id = m2.chat_id AND m1.creation_time = m2.max_time
        """

        rows = db.db.session.execute(text(query), {"ids": tuple(ids)}).fetchall()
        rows_as_dicts = [r._asdict() for r in rows]

        # Build response with chat data, preview messages, and usernames
        chats_as_dict_list = []
        for c, username in chats:
            chat_data = c.to_dict()
            preview_row = next((r for r in rows_as_dicts if r["chat_id"] == chat_data["id"]), None)
            if preview_row:
                chat_data["preview"] = preview_row["message"]
                chat_data["username"] = username  # Use the username from the first query
                chats_as_dict_list.append(chat_data)

        return json.dumps(chats_as_dict_list, indent=4, default=str), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error, " + e}), 500


@chat_route.route('/change-name', methods=['PUT'])
def change_name():
    try:
        if not rest_validation.validate_content_type(request):
            return 'Content-Type not supported!'

        data = request.get_json()

        if not rest_validation.validate_chat_change_name(data):
            return jsonify({"error": "Invalid input: 'name' and 'chat_id' are required"}), 400

        chat_to_update = (chat.Chat.query
                          .filter(chat.Chat.id == data['chat_id'])
                          .first())

        if not chat_to_update:
            return jsonify({"error": "Chat not found"}), 404

        chat_to_update.name = data['name']

        db.db.session.commit()

        return json.dumps(chat_to_update.to_dict(), indent=4, default=str), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
