import json


def decode_bytes_to_utf8(text: bytes):
    """bytes to str with utf-8 encoding and ignore erros

    >>> type(decode_bytes_to_utf8(b'how are you'))
    <class 'str'>

    :param text:
    :return:
    """
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return text


def json_decode(text: str):
    """decode json string

    >>> dic = json_decode('{"key": "value"}')
    >>> dic
    {'key': 'value'}
    >>> type(dic)
    <class 'dict'>

    :param text:
    :return:
    """
    if isinstance(text, str):
        return json.loads(text)
    return text
