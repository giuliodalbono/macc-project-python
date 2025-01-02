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
