from redis import ConnectionPool, Redis


def connect_db(args):
    redis_pool = ConnectionPool(host=args.DB_HOST, port=args.DB_PORT)
    db = Redis(connection_pool=redis_pool)
    return db
