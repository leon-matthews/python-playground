
import hmac
from pprint import pprint as pp
from typing import Optional


def create_digest(key: str, message: str, max_length: Optional[int] = None) -> str:
    """
    Create digest for HMAC message message authentication.

    An HMAC keyed-hash message authentication code

    For maximum security, when it comes time to compare digests use
    the function `hmac.compare_digest()`.

        >>> create_digest('Dragon69', 'My name is Leon', 16)
        '59b625083f790cb5'

    Args:
        key:
            Key string, for example 'settings.SECRET_KEY'
        message:
            Arbitrary string to create digest for.
        max_length:
            If your application doesn't need the full 128 hexstring from
            the SHA-512 algorithm you can limit it.

    See:
        https://en.wikipedia.org/wiki/HMAC

    Returns:
        Hex string, eg. 'deadbeef'
    """
    key_bytes = key.encode('utf-8')
    message_bytes = message.encode('utf-8')
    digest = hmac.digest(key_bytes, message_bytes, 'sha512').hex()
    if max_length is not None:
        digest = digest[:max_length]
    return digest


if __name__ == '__main__':
    SECRET_KEY = 'Dragon69'
    digest = create_digest(SECRET_KEY, 'Secret!', 32)
    digest2 = create_digest(SECRET_KEY, 'Secret!', 32)

    pp(digest)
    pp(digest2)
    is_equal = hmac.compare_digest(digest, digest2)
    pp(is_equal)
