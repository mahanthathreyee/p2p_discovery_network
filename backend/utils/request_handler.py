def check_request_json(request_json, arguments):
    return all(argument in request_json for argument in arguments)