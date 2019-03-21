from sanic import Sanic
from sanic.exceptions import NotFound, MethodNotSupported
from sanic.log import logger
from sanic.response import redirect, json
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc
from api import session
from api.session import session_bp
from utils.db import connect_db
from utils.responses import Response
from redis.exceptions import ConnectionError


def create_app(args):
    db = connect_db(args)
    session.db = connect_db(args)
    try:
        db.ping()
    except ConnectionError:
        logger.error("Redis server is not available")
        quit()

    app = Sanic("backend_session_server")

    app.static("/favicon-16x16.png", "./static/img/favicon.ico")
    app.static("/favicon.ico", "./static/img/favicon.ico")
    app.blueprint(openapi_blueprint)
    app.blueprint(swagger_blueprint)
    app.blueprint(session_bp)

    @doc.exclude(True)
    @app.route("/")
    async def redirect_api(request):
        return redirect("/swagger")

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
