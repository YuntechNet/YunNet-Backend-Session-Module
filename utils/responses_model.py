from sanic_openapi import doc


# TODO separate to other class
class RequestUUID:
    UUID = doc.String


class ResponseModel:
    code = doc.Integer
    success = doc.Boolean
    fail = doc.Boolean
    data = {}
    result = doc.String


class DbResponseModel:
    success = doc.Boolean
    result = doc.String
    last_touched_ts = doc.String
    create_ts = doc.String
