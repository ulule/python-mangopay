# -*- coding: utf-8 -*-
from .resources import Dispute
from .test_base import BaseTest
from .mocks import get_fixture

import responses


class DisputesTest(BaseTest):
    @responses.activate
    def test_retrieve_disputes(self):
        self.register_mock([{
            'method': responses.GET,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/disputes',
            'body': get_fixture('disputes'),
            'status': 200
        }])
        self.assertEqual(len(Dispute.all()), 10)
        self.assertEqual(Dispute.all()[0].dispute_type, 'NOT_CONTESTABLE')
