# -*- coding: utf-8 -*-
from .resources import BankAccount, BankWirePayOut
from .test_base import BaseTest

from mangopay.utils import Money

import responses


class PayOutsTest(BaseTest):
    @responses.activate
    def test_create_bank_wire_payout(self):
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169420/bankaccounts/IBAN',
                'body': {
                    "UserId": "1169420",
                    "Type": "IBAN",
                    "OwnerName": "MangoPay",
                    "OwnerAddress": "1 rue MangoPay, Paris",
                    "IBAN": "FR3020041010124530725S03383",
                    "BIC": "CRLYFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/payouts/bankwire',
                'body': {
                    "Id": 30047,
                    "CreditedFunds": None,
                    "BankWireRef": "John Doe's trousers",
                    "DebitedFunds": {"Currency": "EUR", "Amount": 1000},
                    "BankAccountId": 6784645,
                    "AuthorId": 6784642,
                    "Tag": "Custom data",
                    "Fees": {"Currency": "EUR", "Amount": 100},
                    "DebitedWalletId": 6784644
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/payouts/30047',
                'body': {
                    "Id": 30047,
                    "Tag": "custom tag",
                    "CreationDate": 1374232891,
                    "AuthorId": "20164",
                    "CreditedUserId": None,
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 100
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": "1000"
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": "100"
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "00000",
                    "ExecutionDate": 1374233532,
                    "Type": "PAY_OUT",
                    "Nature": "NORMAL",
                    "DebitedWalletId": "30025",
                    "BankAccountId": "30027",
                    "BankWireRef": "John Doe's trousers"
                },
                'status': 200
            }])

        params = {
            "owner_name": "Victor Hugo",
            "user": self.legal_user,
            "type": "IBAN",
            "owner_address": "1 rue des Misérables",
            "iban": "FR3020041010124530725S03383",
            "bic": "CRLYFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()

        bank_wire_payout_params = {
            "tag": "Custom data",
            "author": self.legal_user,
            "debited_funds": Money(amount=1000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "debited_wallet": self.legal_user_wallet,
            "bank_account": bankaccount,
            "bank_wire_ref": "John Doe's trousers"
        }
        bank_wire_payout = BankWirePayOut(**bank_wire_payout_params)

        self.assertIsNone(bank_wire_payout.get_pk())
        bank_wire_payout.save()
        self.assertIsInstance(bank_wire_payout, BankWirePayOut)

        self.assertEqual(bank_wire_payout.debited_funds.amount, 1000)
        bank_wire_payout_params.pop('debited_funds')

        self.assertEqual(bank_wire_payout.fees.amount, 100)
        bank_wire_payout_params.pop('fees')

        for key, value in bank_wire_payout_params.items():
            self.assertEqual(getattr(bank_wire_payout, key), value)

        self.assertIsNotNone(bank_wire_payout.get_pk())

        # test_retrieve_payouts
        retrieved_payout = BankWirePayOut.get(bank_wire_payout.get_pk())

        self.assertIsNotNone(retrieved_payout.get_pk())
        self.assertIsInstance(retrieved_payout, BankWirePayOut)

        self.assertEqual(getattr(retrieved_payout, 'id'), bank_wire_payout.get_pk())
