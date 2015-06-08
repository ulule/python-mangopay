# -*- coding: utf-8 -*-
from .resources import BankAccount
from .test_base import BaseTest

from datetime import date

import responses
import time


class BankAccountsTest(BaseTest):
    @responses.activate
    def test_create_bankaccount_iban(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/IBAN',
            'body': {
                "UserId": "1169419",
                "Type": "IBAN",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": "1 rue des Misérables",
                "IBAN": "FR3020041010124530725S03383",
                "BIC": "CRLYFRPP",
                "Id": "1169675",
                "Tag": "custom tag",
                "CreationDate": 1383561267
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "IBAN",
            "owner_address": "1 rue des Misérables",
            "iban": "FR3020041010124530725S03383",
            "bic": "CRLYFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_gb(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/GB',
            'body': {
                "UserId": "1169419",
                "Type": "GB",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": "1 rue des Misérables",
                "AccountNumber": "62136016",
                "SortCode": "404865",
                "Id": "38290008",
                "Tag": "custom tag",
                "CreationDate": 1383561267
            },
            'status': 200
        })

        params = {
            "tag": "custom tag",
            "user": self.natural_user,
            "type": "GB",
            "owner_name": "Victor Hugo",
            "owner_address": "1 rue des Misérables",
            "account_number": "62136016",
            "sort_code": "404865"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_us(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/US',
            'body': {
                "UserId": "1169419",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": "1 rue des Misérables",
                "Type": "US",
                "Id": "6775383",
                "Tag": "custom tag",
                "CreationDate": 1431964711,
                "AccountNumber": "123",
                "ABA": "123456789",
                "DepositAccountType": "CHECKING"
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "US",
            "owner_address": "1 rue des Misérables",
            "tag": "custom tag",
            "account_number": "123",
            "aba": "123456789",
            "deposit_account_type": "CHECKING"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_ca(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/CA',
            'body': {
                "UserId": "1169419",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": "1 rue des Misérables",
                "Type": "CA",
                "Id": "6775449",
                "Tag": "custom tag",
                "CreationDate": 1431964854,
                "AccountNumber": "123",
                "InstitutionNumber": "1234",
                "BranchCode": "12345",
                "BankName": "banque nationale of canada"
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "CA",
            "owner_address": "1 rue des Misérables",
            "tag": "custom tag",
            "bank_name": "banque nationale of canada",
            "institution_number": "1234",
            "branch_code": "12345",
            "account_number": "123"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_other(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/OTHER',
            'body': {
                "UserId": "1169419",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": "1 rue des Misérables",
                "Type": "OTHER",
                "Id": "6775453",
                "Tag": "custom tag",
                "CreationDate": 1431964920,
                "AccountNumber": "123",
                "BIC": "CRLYFRPP",
                "Country": "FR"
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "OTHER",
            "owner_address": "1 rue des Misérables",
            "country": "FR",
            "bic": "CRLYFRPP",
            "tag": "custom tag",
            "account_number": "123"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_retrieve_bankaccount_iban(self):
        self.mock_natural_user()
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/IBAN',
                'body': {
                    "UserId": "1169419",
                    "Type": "IBAN",
                    "OwnerName": "Victor Hugo",
                    "OwnerAddress": "1 rue des Misérables",
                    "IBAN": "FR3020041010124530725S03383",
                    "BIC": "CRLYFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/1169675',
                'body': {
                    "UserId": "1169419",
                    "Type": "IBAN",
                    "OwnerName": "Victor Hugo",
                    "OwnerAddress": "1 rue des Misérables",
                    "IBAN": "FR3020041010124530725S03383",
                    "BIC": "CRLYFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts',
                'body': [
                    {
                        "UserId": "1169419",
                        "Type": "IBAN",
                        "OwnerName": "Victor Hugo",
                        "OwnerAddress": "1 rue des Misérables",
                        "IBAN": "FR3020041010124530725S03383",
                        "BIC": "CRLYFRPP",
                        "Id": "1169675",
                        "Tag": "custom tag",
                        "CreationDate": 1383561267
                    }
                ],
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419',
                'body': {
                    "Id": 1169419,
                    "FirstName": "Victor",
                    "LastName": "Hugo",
                    "Address": "1 rue des Misérables, Paris",
                    "Birthday": int(time.mktime(date.today().timetuple())),
                    "Nationality": "FR",
                    "CountryOfResidence": "FR",
                    "Occupation": "Writer",
                    "IncomeRange": 6,
                    "PersonType": "NATURAL",
                    "Email": "victor@hugo.com",
                    "Tag": "custom tag"
                },
                'status': 200
            }])

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "IBAN",
            "owner_address": "1 rue des Misérables",
            "iban": "FR3020041010124530725S03383",
            "bic": "CRLYFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()

        self.assertIsNotNone(bankaccount.get_pk())

        pk = bankaccount.get_pk()

        bankaccount = BankAccount.get(bankaccount.get_pk(), **{'user_id': self.natural_user.get_pk()})

        self.assertIsNotNone(bankaccount.get_pk())

        self.assertEqual(self.natural_user.bankaccounts.get(pk, **{'user_id': self.natural_user.get_pk()}), bankaccount)
        self.assertEqual(self.natural_user.bankaccounts.all(), [bankaccount])

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

    @responses.activate
    def test_retrieve_users_all_bankaccounts(self):
        self.mock_natural_user()
        self.register_mock([
            {
                'method': responses.POST,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts/IBAN',
                'body': {
                    "UserId": "1167502",
                    "Type": "IBAN",
                    "OwnerName": "Victor Hugo",
                    "OwnerAddress": "1 rue des Misérables",
                    "IBAN": "FR3020041010124530725S03383",
                    "BIC": "CRLYFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': 'https://api.sandbox.mangopay.com/v2/chouette/users/1169419/bankaccounts',
                'body': [
                    {
                        "UserId": "1167502",
                        "Type": "IBAN",
                        "OwnerName": "Victor Hugo",
                        "OwnerAddress": "1 rue des Misérables",
                        "IBAN": "FR3020041010124530725S03383",
                        "BIC": "CRLYFRPP",
                        "Id": "1169675",
                        "Tag": "custom tag",
                        "CreationDate": 1383561267
                    }
                ],
                'status': 200
            }])

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "IBAN",
            "owner_address": "1 rue des Misérables",
            "iban": "FR3020041010124530725S03383",
            "bic": "CRLYFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()
        self.assertIsNotNone(bankaccount.get_pk())

        self.assertIsInstance(self.natural_user.bankaccounts.all(), list)

        for bankaccount in self.natural_user.bankaccounts.all():
            self.assertIsInstance(bankaccount, BankAccount)
