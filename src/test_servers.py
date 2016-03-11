# _*_coding: utf-8 _*_
import pytest


def test_method_error():
    """Test the parse_request GET error."""
    from server import parse_request
    with pytest.raises(RuntimeError):
        parse_request("PUT 127.0.0.1:5000 HTTP/1.1 \nHost:127.0.0.1\r\n")


def test_version_error():
    """Test if the HHTP-version is correct."""
    from server import parse_request
    with pytest.raises(RuntimeError):
        parse_request("GET 127.0.0.1:5000 HTTP/3.1 \nHost:127.0.0.1\r\n")


def test_host_error():
    """Test if the host Header is correct."""
    from server import parse_request
    with pytest.raises(RuntimeError):
        parse_request("GET 127.0.0.1:5000 HTTP/1.1 \nHos:127.0.0.1\r\n")
