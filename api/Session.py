from datetime import timedelta, datetime
from json import dumps

from sanic import Blueprint
from sanic.log import logger
from sanic.response import json
from sanic_openapi import doc

from utils.responses import SuccessResponse, FailResponse

session_bp = Blueprint("Session")
db = None


@doc.route(summary="Check user session")
@session_bp.get("/Session/<UUID>", strict_slashes=True)
async def check_session(request, UUID):
    try:
        date_string = db.hget(UUID, "datetime")
    except Exception as e:
        logger.error(e)
        response = FailResponse(True, e)
        return json(vars(response))

    result = SuccessResponse(True,
                             {"code": 0,
                              "result": "Session valid"})
    if date_string is None:
        result = SuccessResponse(True,
                                 {"code": 1, "result": "Session not exist"})
        return json(result)

    date_string = date_string.decode("utf-8")
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    if datetime.now() - date > timedelta(days=30):
        result = SuccessResponse(True,
                                 {"code": 2, "result": "Session expired"})
        return json(result)

    return json(result)


class UUIDreq:
    UUID = str


@doc.route(summary="Add user session")
@session_bp.post("/Session", strict_slashes=True)
@doc.consumes(UUIDreq, content_type="application/json", location="body")
async def add_session(request):
    """
    Request format
    {
        "UUID":str
    }
    """
    try:
        field_pair = {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      "json": dumps(request.json)}
        UUID = request.json["UUID"]
        db.hmset(UUID, field_pair)
        logger.warning("{} added to db".format(UUID))
        response = SuccessResponse(True, {"code": 0,
                                          "result": "Session added"})
    except Exception as e:
        logger.error(e)
        logger.error(request.body)
        response = FailResponse(True, e)
    return json(vars(response))
