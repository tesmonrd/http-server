# _*_utf8_*_


def test_shorter():
    from client import client
    message = "test"
    assert client(message) == message


def test_longer():
    from client import client
    message = "testingtestingtestingtestingtesting"
    assert client(message) == message


def test_exact():
    from client import client
    message = "12345678"
    assert client(message) == message


def test_non_ascii():
    from client import client
    message = "∅∀"
    assert client(message) == message
