class Response:
    def __init__(self, code=0, success=False, fail=False, data={}, result=""):
        self.code = code
        self.success = success
        self.fail = fail
        self.data = data
        self.result = result
