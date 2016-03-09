# _*_utf8_*_


def test_client():
    from client import client
    message = "!test9"
    assert client("!test9") == message
