from sanic import Sanic
from sanic.exceptions import NotFound, MethodNotSupported
from sanic.log import logger
from sanic.response import redirect, json
from sanic_openapi import swagger_blueprint, doc
from api.session import create_api as session_api
from utils.db import RedisDb
from utils.responses import Response


def create_app(args):
    """
    Create Sanic app

    :param args: args
    :return: Sanic
    """
    db = RedisDb(args.DB_HOST, args.DB_PORT)

    if db.db_ping() is not True:
        logger.error("Redis server is not available")
        exit(1)

    app = Sanic("backend_session_server")

    # favicon setup
    app.static("/favicon-16x16.png", "./static/img/favicon.ico")
    app.static("/favicon.ico", "./static/img/favicon.ico")

    # swagger_api setup
    app.blueprint(swagger_blueprint)

    # api register
    session_api(app, db)

    # exception setup
    @doc.exclude(True)
    @app.route("/")
    async def redirect_api(request):
        return redirect("/swagger/")

    @app.exception(NotFound)
    async def page_not_found(request, exception):
        logger.warning(
            "{} try access \"{}\" data: {}".format(request.ip, request.url,
                                                   request.body))
        resp = Response(code=404, fail=True, result="Nothing here :D")
        return json(resp, status=404)

    @app.exception(MethodNotSupported)
    async def method_not_supported(request, exception):
        resp = Response(code=405, fail=True, result="Nothing here :D")
        return json(resp, status=405)

    return app
