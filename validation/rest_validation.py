def validate_content_type(request):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        return True
    else:
        return False


def validate_user(json):
    if json is None or "uid" not in json or "email" not in json or "username" not in json:
        return False

    return True


def validate_chat(json):
    if json is None or "name" not in json or "is_public" not in json or "user_id" not in json:
        return False

    return True


def validate_message(json):
    if json is None or "message" not in json or "translation" not in json or "city" not in json or "chat_id" not in json:
        return False

    return True
