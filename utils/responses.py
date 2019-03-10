class SuccessResponse:
    def __init__(self, code, data):
        self.success = code
        self.data = data


class FailResponse:
    def __init__(self, code, data):
        self.fail = code
        self.reason = data
