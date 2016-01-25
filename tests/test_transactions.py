# -*- coding: utf-8 -*-
from .resources import Transfer, Transaction
from .test_base import BaseTest

from mangopay.utils import Money

from datetime import date

import responses
import time


class TransactionsTest(BaseTest):
    @responses.activate
    def test_retrieve_transactions(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/transfers',
                'body': {
                    "Id": "1169434",
                    "Tag": "DefaultTag",
                    "CreationDate": "2015-05-15",
                    "AuthorId": "1167495",
                    "CreditedUserId": "1167502",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": 900
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": 100
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "ExecutionDate": int(time.mktime(date.today().timetuple())),
                    "Type": "TRANSFER",
                    "Nature": "REGULAR",
                    "DebitedWalletId": "1167496",
                    "CreditedWalletId": "1167504"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/transactions',
                'body': [
                    {
                        "Id": "1174821",
                        "CreationDate": 1385638751,
                        "AuthorId": "1174772",
                        "DebitedFunds": {
                            "Currency": "EUR",
                            "Amount": 500
                        },
                        "CreditedFunds": {
                            "Currency": "EUR",
                            "Amount": 500
                        },
                        "Fees": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Status": "CREATED",
                        "ResultCode": "000000",
                        "ResultMessage": "Success",
                        "ExecutionDate": "2015-05-15",
                        "Type": "TRANSFER",
                        "Nature": "REFUND",
                        "DebitedWalletId": "1174774"
                    }
                ],
                'status': 200,
                'match_querystring': True
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/transactions?status=FAILED&user_id=1169420',
                'body': [
                    {
                        "Id": "1174821",
                        "CreationDate": 1385638751,
                        "AuthorId": "1174772",
                        "DebitedFunds": {
                            "Currency": "EUR",
                            "Amount": 500
                        },
                        "CreditedFunds": {
                            "Currency": "EUR",
                            "Amount": 500
                        },
                        "Fees": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Status": "CREATED",
                        "ResultCode": "000000",
                        "ResultMessage": "Success",
                        "ExecutionDate": "2015-05-15",
                        "Type": "TRANSFER",
                        "Nature": "REFUND",
                        "DebitedWalletId": "1174774"
                    }
                ],
                'status': 200,
                'match_querystring': True
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/transactions?status=FAILED&sort=CreationDate%3Aasc&user_id=1169420',
                'body': [
                    {
                        "Id": "1174821",
                        "CreationDate": 1385638751,
                        "AuthorId": "1174772",
                        "DebitedFunds": {
                            "Currency": "EUR",
                            "Amount": 500
                        },
                        "CreditedFunds": {
                            "Currency": "EUR",
                            "Amount": 500
                        },
                        "Fees": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Status": "FAILED",
                        "ResultCode": "000000",
                        "ResultMessage": "Success",
                        "ExecutionDate": "2015-05-15",
                        "Type": "TRANSFER",
                        "Nature": "REFUND",
                        "DebitedWalletId": "1174774"
                    }
                ],
                'status': 200,
                'match_querystring': True
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/wallets/1169421/transactions',
                'body': [
                    {
                        "Id": "1169215",
                        "Tag": "my transfer",
                        "CreationDate": 1383156787,
                        "AuthorId": "1167492",
                        "CreditedUserId": "1167502",
                        "DebitedFunds": {
                            "Currency": "EUR",
                            "Amount": 100
                        },
                        "CreditedFunds": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Fees": {
                            "Currency": "EUR",
                            "Amount": 100
                        },
                        "Status": "CREATED",
                        "ResultCode": "000000",
                        "ResultMessage": "Success",
                        "ExecutionDate": 1383156788,
                        "Type": "TRANSFER",
                        "Nature": "REGULAR",
                        "CreditedWalletId": "1167504",
                        "DebitedWalletId": "1167494"
                    }
                ],
                'status': 200
            }])

        # Create a transaction:
        params = {
            "author": self.legal_user,
            "credited_user": self.natural_user,
            "debited_funds": Money(amount=1000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "debited_wallet": self.legal_user_wallet,
            "credited_wallet": self.natural_user_wallet,
            "tag": "custom tag"
        }
        transfer = Transfer(**params)
        transfer.save()

        # List user's transactions
        user_transactions = self.legal_user.transactions
        self.assertEqual(len(user_transactions.all()), 1)
        self.assertEqual(user_transactions.all()[0].type, 'TRANSFER')

        # List wallet's transactions
        wallet_transactions = self.legal_user_wallet.transactions
        self.assertEqual(len(wallet_transactions.all()), 1)
        self.assertEqual(wallet_transactions.all()[0].type, 'TRANSFER')

        # List filtered user's transactions
        transactions = Transaction.all(user_id=self.legal_user.get_pk(),
                                       status='FAILED',
                                       sort='CreationDate:asc')
        self.assertEqual(len(transactions), 1)

        transactions = Transaction.all(user_id=self.legal_user.get_pk(), status='FAILED')
        self.assertEqual(len(transactions), 1)
