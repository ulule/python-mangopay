from .utils import Choices


USER_TYPE_CHOICES = Choices(
    ('NATURAL_USER', 'natural', 'Natural user'),
    ('LEGAL_USER', 'legal', 'Legal user')
)

LEGAL_USER_TYPE_CHOICES = Choices(
    ('BUSINESS', 'business', 'Business'),
    ('ORGANIZATION', 'organization', 'Organization')
)

KYC_USER_LEVEL_CHOICES = Choices(
    ('LIGHT', 'light', 'Light'),
    ('REGULAR', 'regular', 'Regular')
)

STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('SUCCEEDED', 'succeeded', 'Succeeded'),
    ('FAILED', 'failed', 'Failed')
)

CARD_TYPE_CHOICES = Choices(
    ('CB_VISA_MASTERCARD', 'cb_visa_mastercard', 'CB VISA MASTERCARD'),
    ('MAESTRO', 'maestro', 'Maestro'),
    ('DINERS', 'diners', 'Diners')
)

PAYMENT_STATUS_CHOICES = Choices(
    ('WAITING', 'waiting', 'Waiting'),
    ('CANCELED', 'canceled', 'Canceled'),
    ('EXPIRED', 'expired', 'Expired'),
    ('VALIDATED', 'validated', 'Validated')
)

VALIDITY_CHOICES = Choices(
    ('UNKNOWN', 'unknown', 'Unknown'),
    ('VALID', 'valid', 'Valid'),
    ('INVALID', 'invalid', 'Invalid')
)

TRANSFER_TYPE_CHOICES = Choices(
    ('PAY_IN', 'payin', 'Pay In'),
    ('PAY_OUT', 'payout', 'Pay out'),
    ('TRANSFER', 'transfer', 'Transfer')
)

NATURE_CHOICES = Choices(
    ('REGULAR', 'regular', 'Regular'),
    ('REFUND', 'refund', 'Refund'),
    ('REPUDIATION', 'repudiation', 'Repudiation')
)

EXECUTION_TYPE_CHOICES = Choices(
    ('WEB', 'web', 'Web'),
    ('DIRECT', 'direct', 'Direct')
)

SECURE_MODE_CHOICES = Choices(
    ('DEFAULT', 'default', 'Default'),
    ('FORCE', 'force', 'Force')
)

BANK_ACCOUNT_TYPE_CHOICES = Choices(
    ('IBAN', 'iban', 'Iban'),
    ('GB', 'gb', 'GB'),
    ('US', 'us', 'US'),
    ('CA', 'ca', 'CA'),
    ('OTHER', 'other', 'Other')
)

DEPOSIT_CHOICES = Choices(
    ('CHECKING', 'checking', 'Checking'),
    ('SAVINGS', 'savings', 'Savings'),
)

DOCUMENTS_TYPE_CHOICES = Choices(
    ('IDENTITY_PROOF', 'identity_proof', 'Identity proof'),
    ('REGISTRATION_PROOF', 'registration_proof', 'Registration proof'),
    ('ARTICLES_OF_ASSOCIATION', 'articles_of_association', 'Articles of association'),
    ('SHAREHOLDER_DECLARATION', 'shareholder_declaration', 'Shareholder Declaration'),
    ('ADDRESS_PROOF', 'address_proof', 'Address Proof')
)

DOCUMENTS_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('VALIDATION_ASKED', 'validation_asked', 'Validation asked'),
    ('VALIDATED', 'validated', 'Validated'),
    ('REFUSED', 'refused', 'Refused')
)

EVENT_TYPE_CHOICES = Choices(
    ('KYC_CREATED', 'kyc_created', 'KYC Created'),
    ('KYC_SUCCEEDED', 'kyc_succeeded', 'KYC succeeded'),
    ('KYC_FAILED', 'kyc_failed', 'KYC failed'),
    ('KYC_VALIDATION_ASKED', 'kyc_validation_asked', 'KYC Validation asked'),
    ('PAYIN_NORMAL_CREATED', 'payin_normal_created', 'Payin normal created'),
    ('PAYIN_NORMAL_SUCCEEDED', 'payin_normal_succeeded', 'Payin normal succeeded'),
    ('PAYIN_NORMAL_FAILED', 'payin_normal_failed', 'Payin normal failed'),
    ('PAYOUT_NORMAL_CREATED', 'payout_normal_created', 'Payout normal created'),
    ('PAYOUT_NORMAL_SUCCEEDED', 'payout_normal_succeeded', 'Payout normal succeeded'),
    ('PAYOUT_NORMAL_FAILED', 'payout_normal_failed', 'Payout normal failed'),
    ('TRANSFER_NORMAL_CREATED', 'transfer_normal_created', 'Transfer normal created'),
    ('TRANSFER_NORMAL_SUCCEEDED', 'transfer_normal_succeeded', 'Transfer normal succeeded'),
    ('TRANSFER_NORMAL_FAILED', 'transfer_normal_failed', 'Transfer normal failed'),
    ('PAYIN_REFUND_CREATED', 'payin_refund_created', 'Payin refund created'),
    ('PAYIN_REFUND_SUCCEEDED', 'payin_refund_succeeded', 'Payin refund succeeded'),
    ('PAYIN_REFUND_FAILED', 'payin_refund_failed', 'Payin refund failed'),
    ('PAYOUT_REFUND_CREATED', 'payout_refund_created', 'Payout refund created'),
    ('PAYOUT_REFUND_SUCCEEDED', 'payout_refund_succeeded', 'Payout refund succeeded'),
    ('PAYOUT_REFUND_FAILED', 'payout_refund_failed', 'Payout refund failed'),
    ('TRANSFER_REFUND_CREATED', 'transfer_refund_created', 'Transfer refund created'),
    ('TRANSFER_REFUND_SUCCEEDED', 'transfer_refund_succeeded', 'Transfer refund succeeded'),
    ('TRANSFER_REFUND_FAILED', 'transfer_refund_failed', 'Transfer refund failed')
)

NOTIFICATION_STATUS_CHOICES = Choices(
    ('ENABLED', 'enabled', 'Enabled'),
    ('DISABLED', 'disabled', 'Disabled')
)

NOTIFICATION_VALIDITY_CHOICES = Choices(
    ('VALID', 'valid', 'Valid'),
    ('INVALID', 'invalid', 'Invalid')
)

DIRECT_DEBIT_TYPE_CHOICES = Choices(
    ('SOFORT', 'sofort', 'Sofort'),
    ('ELV', 'elv', 'ELV'),
    ('GIROPAY', 'giropay', 'Giropay')
)

TRANSACTION_TYPE_CHOICES = Choices(
    ('PAYIN', 'payin', 'Pay In'),
    ('PAYOUT', 'payout', 'Pay out'),
    ('TRANSFER', 'transfer', 'Transfer')
)

DISPUTES_STATUS_CHOICES = Choices(
    ('CREATED', 'created', 'Created'),
    ('PENDING_CLIENT_ACTION', 'pending_client_action', 'Pending Client Action'),
    ('SUBMITTED', 'submitted', 'Submitted'),
    ('PENDING_BANK_ACTION', 'pending_bank_action', 'Pending Bank Action'),
    ('REOPENED_PENDING_CLIENT_ACTION', 'reopened_pending_client_action', 'Reopened Pending Client Action'),
    ('CLOSED', 'closed', 'Closed')
)

DISPUTE_TYPE_CHOICE = Choices(
    ('CONTESTABLE', 'contestable', 'Contestable'),
    ('NOT_CONTESTABLE', 'not_contestable', 'Not Contestable'),
    ('RETRIEVAL', 'retrieval', 'Retrieval')
)

UBO_DECLARATION_STATUS_CHOICES = Choices(
    ("CREATED", "created", "Created"),
    ("VALIDATION_ASKED", "validation_asked", "Validation Asked"),
    ("VALIDATED", "validated", "Validated"),
    ("REFUSED", "refused", "Refused"),
    ("INCOMPLETE", "incomplete", "Incomplete")
)

UBO_DECLARATION_REFUSED_REASON_CHOICES = Choices(
    ("MISSING_UBO", "missing_ubo", "Missing UBO"),
    ("DECLARATION_DO_NOT_MATCH_UBO_INFORMATION", "declaration_do_not_match_ubo_information", "Declaration Do Not "
                                                                                             "Match UBO Information")
)

DECLARED_UBO_STATUS_CHOICES = Choices(
    ("CREATED", "created", "Created"),
    ("VALIDATED", "validated", "Validated"),
    ("REFUSED", "refused", "Refused")
)

DECLARED_UBO_REFUSED_REASON_CHOICES = Choices(
    ("INVALID_DECLARED_UBO", "invalid_declared_ubo", "Invalid Declared UBO"),
    ("INVALID_UBO_DETAILS", "invalid_ubo_details", "Invalid UBO Details")
)
