from sanic import Sanic, Blueprint
from sanic.exceptions import NotFound
from sanic.log import logger
from sanic.response import json, redirect
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc
from redis import Redis, ConnectionPool, ConnectionError
from datetime import datetime, timedelta
from utils.responses import SuccessResponse, FailResponse
from json import dumps
from argparse import ArgumentParser

app = Sanic("backend_session_server")

# Add online API documents
app.blueprint(swagger_blueprint)
app.blueprint(openapi_blueprint)

session_bp = Blueprint("Session")


# parse config
def process_command():
    parser = ArgumentParser(epilog="For Sanic config ref"
                                   "https://sanic.readthedocs.io/en/latest/"
                                   "sanic/config.html")
    server_group = parser.add_argument_group("Server")
    redis_group = parser.add_argument_group("Redis")
    sanic_group = parser.add_argument_group("Sanic")
    server_group.add_argument("--host", type=str, required=True, dest="HOST")
    server_group.add_argument("--port", type=int, required=True, dest="PORT")
    server_group.add_argument("--worker", type=int, default=2, dest="WORKER")
    redis_group.add_argument("--db-host", type=str, default="127.0.0.1",
                             dest="DB_HOST",
                             help="Redis server ip")
    redis_group.add_argument("--db-port", type=int, default=6379,
                             dest="DB_PORT",
                             help="Redis server port")
    sanic_group.add_argument("--REQUEST-MAX-SIZE", type=int, default=100000000,
                             help="How big a request may be (bytes)")
    sanic_group.add_argument("--REQUEST-BUFFER-QUEUE-SIZE", type=int,
                             default=100,
                             help="Request streaming buffer queue size")
    sanic_group.add_argument("--REQUEST-TIMEOUT", type=int, default=60,
                             help="How long a request can take to arrive "
                                  "(sec)")
    sanic_group.add_argument("--RESPONSE-TIMEOUT", type=int, default=60,
                             help="How long a response can take to process "
                                  "(sec)")
    sanic_group.add_argument("--KEEP-ALIVE", type=bool, default=True,
                             help="Disables keep-alive when False")
    sanic_group.add_argument("--KEEP-ALIVE-TIMEOUT", type=int, default=5,
                             help="How long to hold a TCP connection open "
                                  "(sec)")
    sanic_group.add_argument("--GRACEFUL-SHUTDOWN-TIMEOUT", type=float,
                             default=15.0,
                             help="How long to wait to force close non-idle "
                                  "connection (sec)")
    sanic_group.add_argument("--ACCESS-LOG", type=bool, default=True,
                             help="Disable or enable access log")
    return parser.parse_args()


# REST API naming ref
# https://restfulapi.net/resource-naming/

@doc.exclude(True)
@app.route("/")
async def redirect_api(request):
    return redirect("/swagger")


@app.exception(NotFound)
async def page_not_found(request, exception):
    logger.warn(
        "{} try access \"{}\" data: {}".format(request.ip, request.url,
                                               request.body))
    return json(FailResponse(True, {"Code": 404,
                                    "Result": "Nothing here :D"}))


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
                             {"Code": 0,
                              "Result": "Session valid"})
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
@session_bp.post("/Session/", strict_slashes=True)
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
        db.hmset(request.json["UUID"], field_pair)
        response = SuccessResponse(True, {"Code": 0,
                                          "Result": "Session added"})
    except Exception as e:
        logger.error(e)
        response = FailResponse(True, e)
    return json(vars(response))


if __name__ == "__main__":
    args = process_command()

    redis_pool = ConnectionPool(host=args.DB_HOST, port=args.DB_PORT)
    db = Redis(connection_pool=redis_pool)

    try:
        db.ping()
    except ConnectionError:
        logger.error("Redis server is not available")
        quit()

    app.blueprint(session_bp)
    app.static("/favicon-16x16.png", "./static/img/favicon.ico")
    app.static("/favicon.ico", "./static/img/favicon.ico")

    app.run(host=args.HOST, port=args.PORT, workers=args.WORKER)
