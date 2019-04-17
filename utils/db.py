from redis import ConnectionPool, Redis
from redis.exceptions import ConnectionError
from datetime import datetime
from utils.responses import DbResponse


class RedisDb:

    def __init__(self, host, port):
        self.redis_pool = ConnectionPool(host=host, port=port)
        self.db = Redis(connection_pool=self.redis_pool)

    def db_ping(self):
        """
        Ping database

        :return: bool
        """
        try:
            self.db.ping()
        except ConnectionError as e:
            return False
        return True

    def db_exist(self, UUID):
        """
        Check UUID is exist in database

        :param UUID: Session UUID
        :type UUID: str
        :return: bool
        """
        number = self.db.exists(UUID)
        if number == 0:
            return False
        return True

    def db_get_session(self, UUID):
        """
        Get "create_ts" "last_touched_ts" attribute also will update
        "last_touched_ts" attribute

        :param UUID: Session UUID
        :type UUID: str
        :return: DbResponse
        """
        try:
            last_touched_ts = self.db.hget(UUID,
                                           "last_touched_ts").decode("utf-8")
            create_ts = self.db.hget(UUID, "create_ts").decode("utf-8")
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.hset(UUID, "last_touched_ts", date_now)
            resp = DbResponse(True, "", last_touched_ts, create_ts)
        except Exception as e:
            resp = DbResponse(False, e)
            return resp
        return resp

    def db_set_session(self, UUID):
        """
        Add UUID with current timestamp

        :param UUID: Session UUID
        :type UUID: str
        :return: DbResponse
        """
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        field_pair = {"create_ts": date_now,
                      "last_touched_ts": date_now}
        try:
            self.db.hmset(UUID, field_pair)
            resp = DbResponse(True, "")
            return resp
        except Exception as e:
            resp = DbResponse(False, e)
            return resp
            pass
