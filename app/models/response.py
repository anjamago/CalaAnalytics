def response(status=200, message="OK", data={}) -> dict:
    return {
        'status': status,
        'data': data,
        'message': message
    }
