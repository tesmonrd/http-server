# _*_ utf-8 _*_


def test_response_ok():
    """Test if 200 OK message same when decoded."""
    from server import response_ok
    response = response_ok()
    assert response.decode('utf8') == 'HTTP/1.1 200 OK\nContent-Type: text/plain\n\r\nYou Made It!'


def test_response_error():
    """Test if 500 Error message same when decoded."""
    from server import response_error
    response = response_error()
    assert response.decode('utf8') == 'HTTP/1.1 500 Internal Server Error\nContent-Type: text/plain\n\r\nSomething bad happened!'
