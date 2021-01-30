import base64

from pkg_resources import resource_stream


def load_default_profile_image():
    return resource_stream(__name__, 'default_profile_image.jpg').read()


def bytes_to_base64_string(data: bytes) -> str:
    encoded_string = base64.b64encode(data)
    return encoded_string.decode('utf-8')


def base64_string_to_bytes(data: str) -> bytes:
    base64_bytes = data.encode('utf-8')
    return base64.decodebytes(base64_bytes)
