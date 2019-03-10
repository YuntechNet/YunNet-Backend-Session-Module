from sanic import Sanic
from sanic.exceptions import NotFound, MethodNotSupported
from sanic.log import logger
from sanic.response import redirect, json
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc

from api import Session
from api.Session import session_bp
from utils.db import connect_db
from utils.responses import FailResponse


def create_app(args):
    db = connect_db(args)
    Session.db = connect_db(args)
    try:
        db.ping()
    except ConnectionError:
        logger.error("Redis server is not available")
        quit()

    app = Sanic("backend_session_server")

    @doc.exclude(True)
    @app.route("/")
    async def redirect_api(request):
        return redirect("/swagger")

    @app.exception(NotFound)
    async def page_not_found(request, exception):
        logger.warning(
            "{} try access \"{}\" data: {}".format(request.ip, request.url,
                                                   request.body))
        return json(FailResponse(True, {"code": 404,
                                        "result": "Nothing here :D"}))

    @app.exception(MethodNotSupported)
    async def method_not_supported(request, exception):
        return json(FailResponse(True, {"code": 405,
                                        "result": "Method not supported"}))

    app.blueprint(session_bp)
    app.static("/favicon-16x16.png", "./static/img/favicon.ico")
    app.static("/favicon.ico", "./static/img/favicon.ico")
    app.blueprint(swagger_blueprint)
    app.blueprint(openapi_blueprint)

    return app
