from sanic import Sanic
from sanic.response import json, redirect
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc
import Config
import redis
from datetime import datetime, timedelta
from Responses import SuccessResponse, FailResponse

app = Sanic("backend_session_server")
app.config.from_object(Config)

# Add online API documents
app.blueprint(swagger_blueprint)
app.blueprint(openapi_blueprint)


# REST API naming ref
# https://restfulapi.net/resource-naming/

@app.route("/")
async def redirect_api(request):
    return redirect("/swagger")


@doc.route(summary="Check user session")
@app.get("/CheckSession/<UUID>", strict_slashes=True)
async def check_session(request, UUID):
    date_string = db.hget("sessiondb", UUID).decode("utf-8")
    print(date_string)
    result = SuccessResponse(True, {"Code": 0, "Result": "Session exist and not expire"})
    if date_string is None:
        result = SuccessResponse(True, {"Code": 1, "Result": "Session not exist"})
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    if datetime.now() - date > timedelta(days=30):
        result = SuccessResponse(True, {"Code": 2, "Result": "Session expired"})
    return json(result)


@doc.route(summary="Add user sessoin")
@app.put("AddSession/<UUID>", strict_slashes=True)
async def add_session(request, UUID):
    try:
        reply = db.hsetnx("sessiondb", UUID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if reply == 1:
            response = SuccessResponse(True, {"Code": reply, "Result": "Session added"})
        else:
            response = SuccessResponse(True, {"Code": reply,
                                              "Result": "Session already exists and no operation was performed"})
    except Exception as e:
        print(e)
        response = FailResponse(True, "")
    return json(vars(response))


if __name__ == "__main__":
    redis_pool = redis.ConnectionPool(host=Config.DB_HOST, port=Config.DB_PORT)
    db = redis.Redis(connection_pool=redis_pool)

    try:
        db.ping()
    except redis.ConnectionError:
        print("Redis server is not available")
        quit()

    app.run(host=Config.HOST, port=Config.PORT, workers=Config.WORKER)
