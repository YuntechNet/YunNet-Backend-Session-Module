from datetime import timedelta, datetime
from sanic import Sanic, Blueprint
from sanic.log import logger
from sanic.response import json
from sanic_openapi import doc
from utils.responses import Response
from utils.responses_model import ResponseModel, RequestUUID

blueprint = Blueprint("Session", url_prefix="/Session")


def create_api(app, db):
    """
    Init api

    :param app: App to register
    :type app: Sanic
    :param db: Database connection
    :type db: RedisDb
    """
    app.blueprint(blueprint)
    global redis_db
    redis_db = db


@blueprint.get("/<UUID>", strict_slashes=True)
@doc.route(summary="Check user session")
@doc.produces(ResponseModel)
async def check_session(request, UUID):
    try:
        exist = redis_db.db_exist(UUID)
        data = redis_db.db_get_session(UUID)
        if exist:

            last_touched_ts = datetime.strptime(data.last_touched_ts,
                                                "%Y-%m-%d %H:%M:%S")
            create_ts = datetime.strptime(data.create_ts,
                                          "%Y-%m-%d %H:%M:%S")
            result = Response()
            result.data = data
            if datetime.now() - create_ts > timedelta(days=30):
                result.code = 2
                result.success = True
                result.result = "Session expired"
                return json(result)
            result.code = 0
            result.success = True
            result.result = "Session valid"
        else:  # if key not exist
            result = Response(code=1, success=True,
                              result="Session not exist")
            return json(result)
    except Exception as e:
        logger.error(e)
        resp = Response(code=-1, fail=True, result=e)
        return json(vars(resp))
    return json(result)


@blueprint.post("/")
@doc.route(summary="Add user session")
@doc.consumes(RequestUUID, content_type="application/json", location="body")
@doc.produces(ResponseModel, content_type="application/json")
async def add_session(request):
    try:
        UUID = request.json["UUID"]
        redis_db.db_set_session(UUID)
        logger.info("{} added to db".format(UUID))
        resp = Response(code=0, success=True, result="Session added")
    except Exception as e:
        logger.error(e)
        logger.error(request.body)
        resp = Response(code=-1, fail=True, result=e)
    return json(vars(resp))
