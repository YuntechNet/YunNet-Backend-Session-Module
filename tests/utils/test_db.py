from redis import Redis


# TODO(biboy1999):need more test

def test_db_ping(db):
    resp = db.db_ping()
    assert resp is True


def test_db_exist(db):
    resp = db.db_exist('UUID_NOT_EXIST')
    assert resp is False


def test_set_session(db):
    resp = db.db_set_session('UUID_1')
    assert resp.success is True
    assert resp.result is ""
    assert resp.last_touched_ts is ""
    assert resp.create_ts is ""


def test_get_session(db):
    # should I flushdb first?
    resp = db.db_get_session('UUID_1')
    assert resp.success is True
    assert resp.result is ""
    assert resp.last_touched_ts is not ""
    assert resp.create_ts is not ""
