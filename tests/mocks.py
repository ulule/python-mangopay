# -*- coding: utf-8 -*-
import unittest

from datetime import date

import responses
import json
import time
import sys
import re
import os


def get_fixture(name):
    path = os.path.abspath(__file__)
    fixtures_path = os.path.join(os.path.dirname(path), 'fixtures')
    filepath = os.path.join(fixtures_path, '%s.json' % name)

    if sys.version_info < (3, 0):
        with open(filepath, 'r') as file:
            return file.read()

    with open(filepath, newline='', encoding='utf-8') as file:
        return file.read()


class RegisteredMocks(unittest.TestCase):
    def register_mock(self, data):
        match_querystring = False

        if 'match_querystring' in data:
            match_querystring = data['match_querystring'] or False

        if isinstance(data, list):
            for d in data:
                self.register_mock(d)
        else:
            if isinstance(data['body'], (dict, list)):
                data['body'] = json.dumps(data['body'])

            responses.add(data['method'], data['url'],
                          body=data['body'], status=data['status'],
                          content_type='application/json',
                          match_querystring=match_querystring)

    def mock_natural_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/natural',
            'body': get_fixture('natural_user') % time.mktime(date.today().timetuple()),
            'status': 200
        })

    def mock_declarative_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/natural',
            'body': get_fixture('declarative_user') % time.mktime(date.today().timetuple()),
            'status': 200
        })

    def mock_legal_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/legal',
            'body': get_fixture('legal_user') % time.mktime(date.today().timetuple()),
            'status': 200
        })

    def mock_user_wallet(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets',
            'body': get_fixture('user_wallet'),
            'status': 200
        })

    def mock_natural_user_wallet(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets',
                'body': get_fixture('natural_user_wallet'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets/1169420',
                'body': get_fixture('natural_user_wallet'),
                'status': 200
            }])

    def mock_legal_user_wallet(self):
        return self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets',
                'body': get_fixture('legal_user_wallet'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets/1169421',
                'body': get_fixture('legal_user_wallet'),
                'status': 200
            }])

    def mock_natural_user_wallet_9(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets',
                'body': get_fixture('natural_user_wallet_9'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets/1169420',
                'body': get_fixture('natural_user_wallet_9'),
                'status': 200
            }])

    def mock_legal_user_wallet_89(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets',
                'body': get_fixture('legal_user_wallet_89'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets/1169421',
                'body': get_fixture('legal_user_wallet_89'),
                'status': 200
            }])

    def mock_legal_user_wallet_99(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets',
                'body': get_fixture('legal_user_wallet_99'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets/1169421',
                'body': get_fixture('legal_user_wallet_99'),
                'status': 200
            }])

    def mock_card(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/cardregistrations',
                'body': get_fixture('cardregistrations'),
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': re.compile(r'https://api.sandbox.mangopay.com/v2/chouette/cardregistrations/\d+'),
                'body': get_fixture('cardregistrations_update'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': re.compile(r'https://api.sandbox.mangopay.com/v2/chouette/cards/\d+'),
                'body': get_fixture('card'),
                'status': 200
            }])

    def mock_tokenization_request(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://homologation-webpayment.payline.com/webpayment/getToken',
            'body': "data=gcpSOxwNHZutpFWmFCAYQu1kk25qPfJFdPaHT9kM3gKumDF3GeqSw8f-k8nh-s5OC3GNnhGoFONuAyg1RZQW6rVXooQ_ysKsz09HxQFEJfb-6H4zbY2Nnp1TliwkEFi4",
            'status': 200
        })

    def mock_user_list_full(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users',
            'body': get_fixture('user_list_full'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_2_per_page_page1(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users?page=1&per_page=2',
            'body': get_fixture('user_list_2_per_page_page1'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_3_per_page_page2(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users?page=2&per_page=3',
            'body': get_fixture('user_list_3_per_page_page2'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_page1(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users?page=1',
            'body': get_fixture('user_list_page1'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_2_per_page(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users?per_page=2',
            'body': get_fixture('user_list_2_per_page'),
            'status': 200,
            'match_querystring': True
        })

    def mock_ubo_declaration(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations',
            'body': get_fixture('ubo_declaration') % '"Default Tag"',
            'status': 200
        })

    def mock_list_ubo_declarations(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations',
            'body': get_fixture('list_ubo_declarations') % '"Default Tag"',
            'status': 200
        })

    def mock_get_ubo_declaration(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations/122341',
            'body': get_fixture('ubo_declaration') % '"Default Tag"',
            'status': 200
        })

    def mock_ubo_creation(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations/122341/ubos',
            'body': get_fixture('ubo'),
            'status': 200
        })

    def mock_get_ubo(self):
        self.register_mock({
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations/122341/ubos/1232432',
            'body': get_fixture('ubo'),
            'status': 200
        })

    def mock_submit_ubo_declaration(self):
        self.register_mock({
            'method': responses.PUT,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations/122341',
            'body': get_fixture('ubo_declaration_submit') % '"Default Tag"',
            'status': 200
        })

    def mock_update_ubo(self):
        self.register_mock({
            'method': responses.PUT,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/11694190/kyc/ubodeclarations/122341/ubos/1232432',
            'body': get_fixture('ubo_update'),
            'status': 200
        })
