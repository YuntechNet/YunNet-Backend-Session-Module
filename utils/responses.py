class SuccessResponse:
    def __init__(self, code, data):
        self.Success = code
        self.Data = data


class FailResponse:
    def __init__(self, code, data):
        self.Fail = code
        self.Reason = data
