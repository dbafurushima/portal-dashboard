import json


def decode_bytes_to_utf8(text: bytes):
    if isinstance(text, bytes):
        return text.decode('utf-8', errors='ignore')
    return text


def json_decode(text: str):
    if isinstance(text, str):
        return json.loads(text)
    return text