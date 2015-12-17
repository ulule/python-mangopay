import sys

try:
    from .credentials import *  # noqa
except ImportError:
    sys.stderr.write('Error: Can\'t find the file credentials.py')

    MANGOPAY_CLIENT_ID = None
    MANGOPAY_PASSPHRASE = None
    MANGOPAY_API_URL = 'https://api.mangopay.com/v2/'
    MANGOPAY_API_SANDBOX_URL = 'https://api.sandbox.mangopay.com/v2/'
    MANGOPAY_USE_SANDBOX = True
    MANGOPAY_API_VERSION = 2

MOCK_TESTS_RESPONSES = True
