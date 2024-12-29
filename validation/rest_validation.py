def validate_content_type(request):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        return True
    else:
        return False


def validate_user(json):
    if not json or not json.get('uid') or not json.get('email') or not json.get('username'):
        return False
