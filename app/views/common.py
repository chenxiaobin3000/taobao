def success(data=None):
    response = {
        'code': 0,
        'msg': 'success'
    }
    if data is not None:
        response['data'] = data
    return response


def failed(msg, code=-1):
    return {
        'code': code,
        'msg': msg,
        'data': {}
    }
