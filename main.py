from api import session
from server import create_app
from argparse import ArgumentParser


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
    redis_group.add_argument("--db-host", type=str, required=True,
                             dest="DB_HOST",
                             help="Redis server ip")
    redis_group.add_argument("--db-port", type=int, required=True,
                             dest="DB_PORT",
                             help="Redis server port")
    sanic_group.add_argument("--REQUEST-MAX-SIZE", type=int,
                             help="How big a request may be (bytes)")
    sanic_group.add_argument("--REQUEST-BUFFER-QUEUE-SIZE", type=int,

                             help="Request streaming buffer queue size")
    sanic_group.add_argument("--REQUEST-TIMEOUT", type=int,
                             help="How long a request can take to arrive "
                                  "(sec)")
    sanic_group.add_argument("--RESPONSE-TIMEOUT", type=int,
                             help="How long a response can take to process "
                                  "(sec)")
    sanic_group.add_argument("--KEEP-ALIVE", type=bool,
                             help="Disables keep-alive when False")
    sanic_group.add_argument("--KEEP-ALIVE-TIMEOUT", type=int,
                             help="How long to hold a TCP connection open "
                                  "(sec)")
    sanic_group.add_argument("--GRACEFUL-SHUTDOWN-TIMEOUT", type=float,
                             help="How long to wait to force close non-idle "
                                  "connection (sec)")
    sanic_group.add_argument("--ACCESS-LOG", type=bool,
                             help="Disable or enable access log")
    return parser.parse_args()


# REST API naming ref
# https://restfulapi.net/resource-naming/

if __name__ == "__main__":
    args = process_command()
    app = create_app(args)
    app.run(host=args.HOST, port=args.PORT, workers=args.WORKER)
