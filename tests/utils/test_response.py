from utils.responses import SuccessResponse, FailResponse


def test_sucess_res():
    sr = SuccessResponse(code=123, data=456)
    assert sr.success is 123
    assert sr.data is 456
    assert hasattr(sr, 'fail') is False


def test_fail_res():
    fr = FailResponse(code=234, data=567)
    assert fr.fail is 234
    assert fr.reason is 567
    assert hasattr(fr, 'success') is False
