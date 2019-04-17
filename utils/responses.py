class Response:
    def __init__(self, code=0, success=False, fail=False, data={}, result=""):
        self.code = code
        self.success = success
        self.fail = fail
        self.data = data
        self.result = result


class DbResponse:
    def __init__(self, success, result, last_touched_ts="", create_ts=""):
        self.success = success
        self.result = result
        self.last_touched_ts = last_touched_ts
        self.create_ts = create_ts
