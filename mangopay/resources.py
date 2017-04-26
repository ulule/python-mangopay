import six

from . import constants
from .base import BaseApiModel

from .fields import (PrimaryKeyField, EmailField, CharField,
                     BooleanField, DateTimeField, DateField,
                     ManyToManyField, ForeignKeyField,
                     MoneyField, IntegerField, DisputeReasonField)

from .compat import python_2_unicode_compatible
from .query import InsertQuery, UpdateQuery, SelectQuery


class BaseModel(BaseApiModel):
    id = PrimaryKeyField(api_name='Id', required=True)
    tag = CharField(api_name='Tag')
    update_date = DateTimeField(api_name='UpdateDate')


@python_2_unicode_compatible
class User(BaseModel):
    email = EmailField(api_name='Email', required=True)
    person_type = CharField(api_name='PersonType',
                            choices=constants.USER_TYPE_CHOICES,
                            default=constants.USER_TYPE_CHOICES.natural,
                            required=True)
    kyc_level = CharField(
        api_name='KYCLevel',
        default=constants.KYC_USER_LEVEL_CHOICES.light,
        choices=constants.KYC_USER_LEVEL_CHOICES)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users'

    @classmethod
    def cast(cls, result):
        if 'PersonType' in result:
            if result['PersonType'] == 'NATURAL':
                return NaturalUser
            elif result['PersonType'] == 'LEGAL':
                return LegalUser

        return cls

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class NaturalUser(User):
    first_name = CharField(api_name='FirstName', required=True)
    last_name = CharField(api_name='LastName', required=True)
    address = CharField(api_name='Address')
    birthday = DateField(api_name='Birthday')
    nationality = CharField(api_name='Nationality', required=True)
    country_of_residence = CharField(api_name='CountryOfResidence', required=True)
    occupation = CharField(api_name='Occupation')
    income_range = CharField(api_name='IncomeRange')
    proof_of_identity = CharField(api_name='ProofOfIdentity')
    proof_of_address = CharField(api_name='ProofOfAddress')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users/natural'

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class LegalUser(User):
    name = CharField(api_name='Name', required=True)
    legal_person_type = CharField(api_name='LegalPersonType',
                                  choices=constants.LEGAL_USER_TYPE_CHOICES,
                                  default=constants.LEGAL_USER_TYPE_CHOICES.organization,
                                  required=True)
    headquarters_address = CharField(api_name='HeadquartersAddress')
    legal_representative_first_name = CharField(api_name='LegalRepresentativeFirstName', required=True)
    legal_representative_last_name = CharField(api_name='LegalRepresentativeLastName', required=True)
    legal_representative_address = CharField(api_name='LegalRepresentativeAddress')
    legal_representative_email = EmailField(api_name='LegalRepresentativeEmail')
    legal_representative_birthday = DateField(api_name='LegalRepresentativeBirthday', required=True)
    legal_representative_nationality = CharField(api_name='LegalRepresentativeNationality', required=True)
    legal_representative_country_of_residence = CharField(api_name='LegalRepresentativeCountryOfResidence', required=True)
    statute = CharField(api_name='Statute')
    proof_of_registration = CharField(api_name='ProofOfRegistration')
    shareholder_declaration = CharField(api_name='ShareholderDeclaration')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users/legal'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Wallet(BaseModel):
    owners = ManyToManyField(User, api_name='Owners', related_name='wallets', required=True)
    description = CharField(api_name='Description', required=True)
    currency = CharField(api_name='Currency', required=True)
    balance = MoneyField(api_name='Balance')
    creation_date = DateField(api_name='CreationDate')

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'
        url = '/wallets'

    def __str__(self):
        return 'Wallet n.%s' % self.id


@python_2_unicode_compatible
class Transfer(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    creation_date = DateField(api_name='CreationDate')
    credited_funds = MoneyField(api_name='CreditedFunds', required=True)
    status = CharField(api_name='Status',
                       choices=constants.STATUS_CHOICES,
                       default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')

    class Meta:
        verbose_name = 'transfer'
        verbose_name_plural = 'transfers'
        url = '/transfers'

    def __str__(self):
        return 'Transfer from wallet %s to wallet %s' % (self.debited_wallet_id, self.credited_wallet_id)


@python_2_unicode_compatible
class Card(BaseModel):
    creation_date = DateField(api_name='CreationDate')
    expiration_date = CharField(api_name='ExpirationDate')
    alias = CharField(api_name='Alias')
    card_provider = CharField(api_name='CardProvider')
    card_type = CharField(api_name='CardType',
                          choices=constants.CARD_TYPE_CHOICES,
                          default=None)
    country = CharField(api_name='Country')
    product = CharField(api_name='Product')
    bank_code = CharField(api_name='BankCode')
    active = BooleanField(api_name='Active')
    currency = CharField(api_name='Currency')
    validity = CharField(api_name='Validity',
                         choices=constants.VALIDITY_CHOICES,
                         default=constants.VALIDITY_CHOICES.unknown)
    user = ForeignKeyField(User, api_name='UserId', required=True, related_name='cards')

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        url = '/cards'

    def __str__(self):
        return '%s of user %s' % (self.card_type, self.user_id)


class CardRegistration(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', required=True, related_name='card_registrations')
    currency = CharField(api_name='Currency', required=True)
    card_type = CharField(api_name='CardType', choices=constants.CARD_TYPE_CHOICES, default=None)
    card_registration_url = CharField(api_name='CardRegistrationURL')
    registation_data = CharField(api_name='RegistrationData')
    access_key = CharField(api_name='AccessKey')
    preregistration_data = CharField(api_name='PreregistrationData')
    registration_data = CharField(api_name='RegistrationData')
    card = ForeignKeyField(Card, api_name='CardId')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    creation_date = DateField(api_name='CreationDate')

    class Meta:
        verbose_name = 'cardregistration'
        verbose_name_plural = 'cardregistrations'
        url = '/cardregistrations'


class PayIn(BaseModel):
    fees = MoneyField(api_name='Fees', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    credited_funds = MoneyField(api_name='CreditedFunds', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSFER_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType')
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = '/payins'


@python_2_unicode_compatible
class DirectPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    creation_date = DateField(api_name='CreationDate')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/card/direct',
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Direct Payin: %s to %s' % (self.author_id, self.credited_user_id)


@python_2_unicode_compatible
class BankWirePayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    declared_debited_funds = MoneyField(api_name='DeclaredDebitedFunds', required=True)
    declared_fees = MoneyField(api_name='DeclaredFees', required=True)
    wire_reference = CharField(api_name='WireReference')
    bank_account = CharField(api_name='BankAccount')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/bankwire/direct',
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Bank Wire Payin: %s to %s' % (self.author_id, self.credited_user_id)


class CardWebPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    return_url = CharField(api_name='ReturnURL')
    template_url_options = CharField(api_name='TemplateURLOptions')
    culture = CharField(api_name='Culture')
    card_type = CharField(api_name='CardType', choices=constants.CARD_TYPE_CHOICES, default=None)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    redirect_url = CharField(api_name='RedirectURL')

    class Meta:
        verbose_name = 'card_payin'
        verbose_name_plural = 'card_payins'
        url = {
            InsertQuery.identifier: '/payins/card/web',
            SelectQuery.identifier: '/payins'
        }


class DirectDebitWebPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    return_url = CharField(api_name='ReturnURL')
    template_url_options = CharField(api_name='TemplateURLOptions')
    culture = CharField(api_name='Culture')
    direct_debit_type = CharField(api_name='DirectDebitType', choices=constants.DIRECT_DEBIT_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    redirect_url = CharField(api_name='RedirectURL')

    class Meta:
        verbose_name = 'direct_debit_payin'
        verbose_name_plural = 'direct_debit_payins'
        url = {
            InsertQuery.identifier: '/payins/directdebit/web',
            SelectQuery.identifier: '/payins'
        }


class PreAuthorization(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    payment_status = CharField(api_name='PaymentStatus', choices=constants.PAYMENT_STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default,
                            required=True)
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    expiration_date = DateField(api_name='ExpirationDate')
    payin = ForeignKeyField(PayIn, api_name='PayinId')

    class Meta:
        verbose_name = 'preauthorization'
        verbose_name_plural = 'preauthorizations'
        url = {
            InsertQuery.identifier: '/preauthorizations/card/direct',
            UpdateQuery.identifier: '/preauthorizations',
            SelectQuery.identifier: '/preauthorizations'
        }


class PreAuthorizedPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    preauthorization = ForeignKeyField(PreAuthorization, api_name='PreauthorizationId', required=True)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)

    class Meta:
        verbose_name = 'preauthorized_payin'
        verbose_name_plural = 'preauthorized_payins'
        url = {
            InsertQuery.identifier: '/payins/PreAuthorized/direct',
            SelectQuery.identifier: '/payins'
        }


@python_2_unicode_compatible
class BankAccount(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', related_name='bankaccounts')
    owner_name = CharField(api_name='OwnerName', required=True)
    owner_address = CharField(api_name='OwnerAddress', required=True)
    creation_date = DateField(api_name='CreationDate')
    type = CharField(api_name='Type', choices=constants.BANK_ACCOUNT_TYPE_CHOICES, default=None)
    iban = CharField(api_name='IBAN', required=True)
    bic = CharField(api_name='BIC')
    account_number = CharField(api_name='AccountNumber')
    sort_code = CharField(api_name='SortCode')
    aba = CharField(api_name='ABA')
    deposit_account_type = CharField(api_name='DepositAccountType',
                                     choices=constants.DEPOSIT_CHOICES,
                                     default=constants.DEPOSIT_CHOICES.checking)
    bank_name = CharField(api_name='BankName')
    institution_number = CharField(api_name='InstitutionNumber')
    branch_code = CharField(api_name='BranchCode')
    country = CharField(api_name='Country')
    bic = CharField(api_name='BIC')

    class Meta:
        verbose_name = 'bankaccount'
        verbose_name_plural = 'bankaccounts'
        url = {
            InsertQuery.identifier: '/users/%(user_id)s/bankaccounts/%(type)s',
            SelectQuery.identifier: '/users/%(user_id)s/bankaccounts',
        }

    def __str__(self):
        return 'Bank account %s of user %s' % (self.type, self.user_id)


@python_2_unicode_compatible
class BankWirePayOut(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    credited_funds = MoneyField(api_name='CreditedFunds', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId', required=True)
    bank_account = ForeignKeyField(BankAccount, api_name='BankAccountId', required=True)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSFER_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType')
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    bank_wire_ref = CharField(api_name='BankWireRef')

    class Meta:
        verbose_name = 'payout'
        verbose_name_plural = 'payouts'
        url = {
            InsertQuery.identifier: '/payouts/bankwire',
            SelectQuery.identifier: '/payouts'
        }

    def __str__(self):
        return 'PayOut request from user %s' % self.author_id


class Refund(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    credited_funds = MoneyField(api_name='CreditedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSFER_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    refund_reason = CharField(api_name='RefundReason')

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = '/refunds'


@python_2_unicode_compatible
class TransferRefund(Refund):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    transfer = ForeignKeyField(Transfer)

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = {
            InsertQuery.identifier: '/transfers/%(transfer_id)s/refunds',
            SelectQuery.identifier: '/refunds'
        }

    def __str__(self):
        return 'TransferRefund request from user %s' % self.author_id


@python_2_unicode_compatible
class PayInRefund(Refund):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')
    payin = ForeignKeyField(PayIn)

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = {
            InsertQuery.identifier: '/payins/%(payin_id)s/refunds',
            SelectQuery.identifier: '/refunds'
        }

    def __str__(self):
        return 'PayInRefund request from user %s' % self.author_id


class KYC(BaseModel):
    class Meta:
        verbose_name = 'kyc'
        verbose_name_plural = 'kycs'
        url = '/KYC/documents'


@python_2_unicode_compatible
class Document(KYC):
    user = ForeignKeyField(User, related_name='documents', api_name='UserId')
    type = CharField(api_name='Type', choices=constants.DOCUMENTS_TYPE_CHOICES, default=None)
    status = CharField(api_name='Status', choices=constants.DOCUMENTS_STATUS_CHOICES, default=None)
    refused_reason_type = CharField(api_name='RefusedReasonType')
    refused_reason_message = CharField(api_name='RefusedReasonMessage')

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'
        url = '/users/%(user_id)s/KYC/documents'

    def __str__(self):
        return 'Document for user %s' % self.user_id


@python_2_unicode_compatible
class Page(KYC):
    file = CharField(api_name='File', required=True, python_value_callback=lambda value: six.b(value))
    user = ForeignKeyField(User)
    document = ForeignKeyField(Document)

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        url = '/users/%(user_id)s/KYC/documents/%(document_id)s/pages'

    def __str__(self):
        return 'Page of document %s for user %s' % (self.document_id, self.user_id)


@python_2_unicode_compatible
class Transaction(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', related_name='transactions')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')
    debited_funds = MoneyField(api_name='DebitedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSFER_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    wallet = ForeignKeyField(Wallet, related_name='transactions')

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        url = '/users/%(user_id)s/transactions'

    def __str__(self):
        return 'Transaction n.%s' % self.id


class Event(BaseModel):
    resource_id = IntegerField(api_name='ResourceId')
    event_type = CharField(api_name='EventType', choices=constants.EVENT_TYPE_CHOICES, default=None)
    date = DateTimeField(api_name='Date')

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        url = '/events'


class Notification(BaseModel):
    url = CharField(api_name='Url', required=True)
    status = CharField(api_name='Status', choices=constants.NOTIFICATION_STATUS_CHOICES, default=None)
    validity = CharField(api_name='Validity', choices=constants.NOTIFICATION_VALIDITY_CHOICES, default=None)
    event_type = CharField(api_name='EventType', choices=constants.EVENT_TYPE_CHOICES, default=None, required=True)
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        url = '/hooks'


class Dispute(BaseModel):
    initial_transaction_id = CharField(api_name='InitialTransactionId')
    initial_transaction_type = CharField(api_name='InitialTransactionType', choices=constants.TRANSACTION_TYPE_CHOICES,
                                         default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    dispute_reason = DisputeReasonField(api_name='DisputeReason')
    status = CharField(api_name='Status', choices=constants.DISPUTES_STATUS_CHOICES, default=None)
    status_message = CharField(api_name='StatusMessage')
    disputed_funds = MoneyField(api_name='DisputedFunds')
    contested_funds = MoneyField(api_name='ContestedFunds')
    repudiation_id = CharField(api_name='RepudiationId')
    dispute_type = CharField(api_name='DisputeType', choices=constants.DISPUTE_TYPE_CHOICE, default=None)
    contest_deadline_date = DateTimeField(api_name='ContestDeadlineDate')
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'dispute'
        verbose_name_plural = 'disputes'
        url = '/disputes'

    def __str__(self):
        return 'Dispute n.%s tag:%s' % (self.id, self.tag)
