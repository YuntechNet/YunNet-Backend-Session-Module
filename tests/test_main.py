from main import check_session


async def test_redirect_api(test_cli):
    resp = await test_cli.get('/')
    assert resp.status == 200
    assert str(resp.url).endswith('swagger') is True


async def test_404(test_cli):
    resp = await test_cli.get('/this_must_be_404')
    assert resp.status == 200
    jsonRes = await resp.json()
    assert jsonRes['fail'] is True
    assert jsonRes['reason']['Code'] == 404
    assert jsonRes['reason']['Result'] == 'Nothing here :D'


async def test_add_session_wrong_methods(test_cli):
    resp = await test_cli.get('/Session')
    assert resp.status == 405


async def test_check_session_empty_session(test_cli):
    resp = await test_cli.get('/Session/')
    assert resp.status == 200


async def test_check_session_not_exists(test_cli):
    resp = await test_cli.get('/Session/NOT_EXISTS_UUID')
    assert resp.status == 200
    jsonRes = await resp.json()
    print(jsonRes)
    assert jsonRes['success'] is True
    assert jsonRes['reason']['Code'] == 1
    assert jsonRes['reason']['Result'] == 'Session not exist'


async def test_add_session_wrong_methods(test_cli):
    resp = await test_cli.get('/Session')
    assert resp.status == 405


async def test_add_session(test_cli):
    resp = await test_cli.post('/Session', data={'UUID': 'THIS_IS_A_UUID'})
    assert resp.status == 200
    resp = await test_cli.get('/Session/THIS_IS_A_UUID')
    assert resp.status == 200
    jsonRes = await resp.json()
    print(jsonRes)
    assert jsonRes['success'] is True
    assert jsonRes['Code'] == 0
    assert jsonRes['Result'] == 'Session valid'
