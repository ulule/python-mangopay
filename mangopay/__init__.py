client_id = None
passphrase = None
api_url = 'https://api.mangopay.com/v2/'
api_sandbox_url = 'https://api.sandbox.mangopay.com/v2/'
api_version = 2
sandbox = True


from .utils import memoize
from .api import APIRequest  # noqa


def _get_default_handler():
    return APIRequest()

get_default_handler = memoize(_get_default_handler, {}, 0)
