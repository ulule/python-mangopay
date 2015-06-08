import sys

try:
    from . import credentials
except ImportError as e:
    sys.stderr.write('Error: Can\'t find the file credentials.py')
    raise e

MANGOPAY_CLIENT_ID = getattr(credentials, 'MANGOPAY_CLIENT_ID', None)
MANGOPAY_PASSPHRASE = getattr(credentials, 'MANGOPAY_PASSPHRASE', None)
MANGOPAY_API_URL = getattr(credentials, 'MANGOPAY_API_URL', 'https://api.mangopay.com/v2/')
MANGOPAY_API_SANDBOX_URL = getattr(credentials, 'MANGOPAY_API_SANDBOX_URL', 'https://api.sandbox.mangopay.com/v2/')
MANGOPAY_USE_SANDBOX = getattr(credentials, 'MANGOPAY_USE_SANDBOX', True)
MANGOPAY_API_VERSION = getattr(credentials, 'MANGOPAY_API_VERSION', 2)

MOCK_TESTS_RESPONSES = True
