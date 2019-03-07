from sanic import Sanic, Blueprint
from sanic.exceptions import NotFound
from sanic.response import json, redirect, text
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc
import sanic_openapi
import Config
import redis
from datetime import datetime, timedelta
from utils.responses import SuccessResponse, FailResponse

app = Sanic("backend_session_server")
app.config.from_object(Config)

# Add online API documents
app.blueprint(swagger_blueprint)
app.blueprint(openapi_blueprint)

session_bp = Blueprint("Session")


# REST API naming ref
# https://restfulapi.net/resource-naming/

@doc.exclude(True)
@app.route("/")
async def redirect_api(request):
    return redirect("/swagger")


@app.exception(NotFound)
async def page_not_found(request, exception):
    print("{} try access \"{}\" data: {}".format(request.ip, request.url,
                                                 request.body))
    return text("404 Nothing here :D")


@doc.route(summary="Check user session")
@session_bp.get("/Session/<UUID>", strict_slashes=True)
async def check_session(request, UUID):
    try:
        date_string = db.hget("sessiondb", UUID)
    except Exception as e:
        print(e)
        response = FailResponse(True, e)
        return json(vars(response))

    result = SuccessResponse(True,
                             {"Code": 0,
                              "Result": "Session exist and not expire"})
    if date_string is None:
        result = SuccessResponse(True,
                                 {"Code": 1, "Result": "Session not exist"})
        return json(result)

    date_string = date_string.decode("utf-8")
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    if datetime.now() - date > timedelta(days=30):
        result = SuccessResponse(True,
                                 {"Code": 2, "Result": "Session expired"})
        return json(result)

    return json(result)


@doc.route(summary="Add user sessoin")
@session_bp.post("/Session/<UUID>", strict_slashes=True)
async def add_session(request, UUID):
    try:
        reply = db.hsetnx("sessiondb", UUID,
                          datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if reply == 1:
            response = SuccessResponse(True, {"Code": reply,
                                              "Result": "Session added"})
        else:
            response = SuccessResponse(True, {"Code": reply,
                                              "Result": "Session exists"})
    except Exception as e:
        print(e)
        response = FailResponse(True, e)
    return json(vars(response))


if __name__ == "__main__":
    redis_pool = redis.ConnectionPool(host=Config.DB_HOST,
                                      port=Config.DB_PORT)
    db = redis.Redis(connection_pool=redis_pool)

    try:
        db.ping()
    except redis.ConnectionError:
        print("Redis server is not available")
        quit()

    app.blueprint(session_bp)
    app.static("/favicon-16x16.png", "./static/img/favicon.ico")
    app.static("/favicon.ico", "./static/img/favicon.ico")
    app.run(host=Config.HOST, port=Config.PORT, workers=Config.WORKER)
