from datetime import timedelta, datetime
from json import dumps
from sanic import Blueprint
from sanic.log import logger
from sanic.response import json
from sanic_openapi import doc
from utils.responses import Response

session_bp = Blueprint("Session", url_prefix="/Session")
db = None


@session_bp.get("/<UUID>", strict_slashes=True)
@doc.route(summary="Check user session", produces=Response)
async def check_session(request, UUID):
    try:
        exist = db.hexists(UUID, "create_ts")
        if exist == 1:
            last_touched_ts_str = db.hget(UUID, "last_touched_ts")
            last_touched_ts_str = last_touched_ts_str.decode("utf-8")
            last_touched_ts = datetime.strptime(last_touched_ts_str,
                                                "%Y-%m-%d %H:%M:%S")

            create_ts_str = db.hget(UUID, "create_ts")
            create_ts_str = create_ts_str.decode("utf-8")
            create_ts = datetime.strptime(create_ts_str, "%Y-%m-%d %H:%M:%S")

            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.hset(UUID, "last_touched_ts", date_now)

            result = Response()
            result.data = {"create_ts": create_ts_str,
                           "last_touched_ts": last_touched_ts_str}

            if datetime.now() - create_ts > timedelta(days=30):
                result.code = 2
                result.success = True
                result.result = "Session expired"
                return json(result)

            result.code = 0
            result.success = True
            result.result = "Session valid"

        else:  # if key not exist
            result = Response(code=1, success=True, result="Session not exist")
            return json(result)
    except Exception as e:
        logger.error(e)
        resp = Response(code=-1, fail=True, result=e)
        return json(vars(resp))

    return json(result)


@session_bp.post("/")
@doc.route(summary="Add user session")
async def add_session(request):
    """
    Request format
    {
        "UUID":str
    }
    """
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        field_pair = {"create_ts": date_now,
                      "last_touched_ts": date_now,
                      "json": dumps(request.json)}
        UUID = request.json["UUID"]
        db.hmset(UUID, field_pair)
        logger.info("{} added to db".format(UUID))
        resp = Response(code=0, success=True, result="Session added")
    except Exception as e:
        logger.error(e)
        logger.error(request.body)
        resp = Response(code=-1, fail=True, result=e)
    return json(vars(resp))
