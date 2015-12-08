# -*- coding: utf-8 -*-
import requests

from datetime import date
from exam.decorators import fixture

from . import settings
from .mocks import RegisteredMocks
from .resources import (NaturalUser, LegalUser, Wallet,
                        CardRegistration, Card)

import responses
import time


_activate = responses.activate


def override_activate(func):
    if getattr(settings, 'MOCK_TESTS_RESPONSES', True):
        return _activate(func)
    return func

responses.activate = override_activate


class BaseTest(RegisteredMocks):
    @fixture
    def natural_user(self):
        natural_user_params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": "1 rue des Misérables, Paris",
            "birthday": time.mktime(date.today().timetuple()),
            "nationality": "FR",
            "country_of_residence": "FR",
            "occupation": "Writer",
            "income_range": 6,
            "proof_of_identity": None,
            "proof_of_address": None,
            "person_type": "NATURAL",
            "email": "victor@hugo.com",
            "tag": "custom tag",
        }
        natural_user = NaturalUser(**natural_user_params)
        natural_user.save()

        return natural_user

    @fixture
    def legal_user(self):
        legal_user_params = {
            "name": "MangoPay",
            "legal_person_type": "BUSINESS",
            "headquarters_address": "1 rue MangoPay, Paris",
            "legal_representative_first_name": "Mango",
            "legal_representative_last_name": "Pay",
            "legal_representative_email": "mango@mangopay.com",
            "legal_representative_birthday": time.mktime(date.today().timetuple()),
            "legal_representative_nationality": "FR",
            "legal_representative_country_of_residence": "FR",
            "proof_of_registration": None,
            "shareholder_declaration": None,
            "legal_representative_address": None,
            "statute": None,
            "person_type": "LEGAL",
            "email": "info@mangopay.com",
            "tag": "custom tag",
            # "creation_date": datetime.now()
        }
        legal_user = LegalUser(**legal_user_params)
        legal_user.save()

        return legal_user

    @fixture
    def legal_user_wallet(self):
        legal_user_wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.legal_user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }

        legal_user_wallet = Wallet(**legal_user_wallet_params)
        legal_user_wallet.save()

        return legal_user_wallet

    @fixture
    def natural_user_wallet(self):
        natural_user_wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.natural_user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }

        natural_user_wallet = Wallet(**natural_user_wallet_params)
        natural_user_wallet.save()

        return natural_user_wallet

    @fixture
    def card(self):
        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        self.mock_tokenization_request()

        response = requests.post(card_registration.card_registration_url, data={
            'cardNumber': '4970100000000154',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card

    @fixture
    def natural_user_card(self):
        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        self.mock_tokenization_request()

        response = requests.post(card_registration.card_registration_url, data={
            'cardNumber': '4970101122334422',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card

    @fixture
    def legal_user_card(self):
        card_params = {
            "user": self.legal_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        self.mock_tokenization_request()

        response = requests.post(card_registration.card_registration_url, data={
            'cardNumber': '4970101122334406',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card
