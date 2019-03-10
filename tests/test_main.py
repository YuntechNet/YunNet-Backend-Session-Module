from main import check_session


async def test_redirect_api(test_cli):
    resp = await test_cli.get('/')
    assert resp.status is 200
    assert str(resp.url).endswith('swagger') is True


async def test_404(test_cli):
    resp = await test_cli.get('/this_must_be_404')
    assert resp.status is 200
    jsonRes = await resp.json()
    assert jsonRes['fail'] is True
    assert jsonRes['reason']['Code'] == 404
    assert jsonRes['reason']['Result'] == 'Nothing here :D'


async def test_check_session(test_cli):
    resp = await test_cli.get('/Session')
    assert resp.status is 200
    jsonRes = await resp.json()
    assert jsonRes['fail'] is True
    assert jsonRes['reason']['Code'] == 404
    assert jsonRes['reason']['Result'] == 'Nothing here :D'
