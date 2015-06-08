# Usage

## Create an handler

To manipulate resources (Users, Wallets, etc.) from this api you will have to
instanciate a new handler which is a connection authentification.

To create a new handler, you have to provide several parameters:

`MANGOPAY_CLIENT_ID`: Which is the client identifier used by [mangopay](http://www.mangopay.com/) to identify you.

`MANGOPAY_PASSPHRASE`: This is your password.



## API host

The host used to call the API. We will see later
when you are creating a new handler you can choose between
multiple environment hosts already registered.

Let's get to work, we will create our first handler with the sandbox host:

```python

mangopay.client_id='my client id'
mangopay.passphrase='my password'

from mangopay.api import APIRequest

handler = APIRequest(sandbox=True)

```

Now we have a new handler which is using the `sandbox host`.

If you are not specifying that you are using the `sandbox host`
nor an existing host, it will use the `production host`.



## Using resources

To manipulate resources, this library is heavily inspired from [peewee](https://github.com/coleifer/peewee/),
so every operations will be like manipulating an ORM.

For required parameters you have to refer to the [reference api](https://docs.mangopay.com/api-references/).



## User

Create a natural user:

```python

from mangopay.resources import User

natural_user = NaturalUser(first_name='Victor',
                           last_name='Hugo',
                           address='1 rue des Misérables, Paris',
                           birthday=1300186358,
                           nationality='FR',
                           country_of_residence=FR',
                           occupation='Writer',
                           income_range='6',
                           proof_of_identity=None,
                           proof_of_address=None,
                           person_type='NATURAL',
                           email='victor@hugo.com',
                           tag='custom tag')

natural_user.save() # save the new user

print natural_user.get_pk() # retrieve the primary key

```

Retrieve an existing user:

```python

natural_user = NaturalUser.get(1)

print natural_user.first_name # Victor

```

Detect an unexisting user:

```python

try:
    natural_user = NaturalUser.get(2)
except NaturalUser.DoesNotExist:
    print 'The natural user 2 does not exist'

```

Retrieve all users:

```python

users = User.all()
print users  # [<NaturalUser: victor@hugo.com>, <LegalUser: support@ulule.com>]

```

Retrieve users with a pagination:

```python

users = User.all(page=1, per_page=2)

```


## Wallet

Create a wallet:

```python

natural_user = NaturalUser.get(1)

from mangopay.resources import Wallet

wallet = Wallet(owners=[natural_user],
                description='Wallet of Victor Hugo',
                currency='EUR',
                tag='wallet for user n.1')

wallet.save() # save the new wallet

print wallet.get_pk() # 1

print wallet.balance  # EUR 0.00

```

Retrieve user's wallets:

```python

natural_user = NaturalUser.get(1)

print natural_user.wallets  # [<Wallet: Wallet n.1169421>]

```



## Transfer

Create a transfer from a wallet to another one:

```python

print legal_user_wallet.balance  # EUR 99.00
print natural_user_wallet.balance  # EUR 0.00


transfer = Transfer(author=legal_user,
                    credited_user=natural_user,
                    debited_funds=Money(amount=10, currency='EUR'),  # Create a EUR 10.00 transfer
                    fees=Money(amount=1, currency='EUR'),  # With EUR 1.00 of fees
                    debited_wallet=legal_user_wallet,
                    credited_wallet=natural_user_wallet)

transfer.save()


print legal_user_wallet.balance  # EUR 89.00
print natural_user_wallet.balance  # EUR 9.00

```



## Transfer Refund

Transfer money back to the wallet it came from (transfer refund):

```python

print legal_user_wallet.balance  # EUR 89.00
print natural_user_wallet.balance  # EUR 9.00


transfer_refund = TransferRefund(author=legal_user,
                                 transfer_id=transfer.get_pk())

transfer_refund.save()


print natural_user_wallet.balance  # EUR 0.00
print legal_user_wallet.balance  # EUR 99.00

```



## Transactions

Retrieve wallet's transactions:

```python

print legal_user_wallet.transactions.all()  # [<Transaction: Transaction n.1174821>]

```


Retrieve user's transactions:

```python

print legal_user.transactions.all()  # [<Transaction: Transaction n.1174821>]

```


List all transactions made by a user (you can filter transactions by status):

```python

transactions = Transaction.all(user_id=natural_user.get_pk(), status='SUCCEEDED')

print transactions  # [<Transaction: Transaction n.1174821>]

```



## Card

Register a card:

To register a card for a user you have to create a RegistrationCard object with the user and his currency as params:

```python

card_registration = CardRegistration(user=natural_user, currency='EUR')
card_registration.save()

```

Then, you have to retrieve user's cards details through a form and send them to the Mangopay Tokenization server.

Mandatory information are:
* The card number
* The card CVX
* The expiration date

And as hidden field:
* The access key ref
* The preregistered data (from the `card_registration` instance you created just before)


Update the `card_registration` instance with the response provided by the Mangopay Tokenization server:

```python

card_registration.registration_data = response
card_registration.save()

```


We now have a `card_id` and you can retrieve the new card:

```python

print card_registration.card_id  # 1
print card_registration.card  # CB_VISA_MASTERCARD of user 6641810

```


Retrieve user's cards:

```python

print user.cards.all()  # [<Card: CB_VISA_MASTERCARD of user 6641810>]

print user.cards.get(card.id)  # CB_VISA_MASTERCARD of user 6641810

```



## PayIn

Direct payment on a user's wallet:

```python

direct_payin = DirectPayIn(author=natural_user,
                           debited_funds=Money(amount=100, currency='EUR'),
                           fees=Money(amount=1, currency='EUR'),
                           credited_wallet_id=legal_user_wallet,
                           card_id=card,
                           secure_mode=DEFAULT",
                           secure_mode_return_url="https://www.ulule.com/")

direct_payin.save()

print legal_user_wallet.balance  # EUR 99.00

```

### OR

Register a bank account:

```python

bankaccount = BankAccountIBAN(owner_name="Victor Hugo",
                              user=natural_user,
                              type="IBAN",
                              owner_address="1 rue des Misérables",
                              iban="FR3020041010124530725S03383",
                              bic="CRLYFRPP")

bankaccount.save()

```

And pay by bank wire:

```python

bank_wire_payin = BankWirePayIn(credited_user_id=legal_user,
                                credited_wallet_id=legal_user_wallet,
                                declared_debited_funds=Money(amount=100, currency='EUR'),
                                declared_fees=Money(amount=1, currency='EUR'))

bank_wire_payin.save()

print legal_user_wallet.balance  # EUR 99.00

```



## Refund

Refund a user on his payment card:

```python

payin_refund = PayInRefund(author=natural_user,
                           payin=direct_payin)

payin_refund.save()

```



## PayOut

Withdraw money from a wallet to a bank account:

```python

payout = PayOut(author=legal_user,
                       debited_funds=Money(amount=100, currency='EUR'),
                       fees=Money(amount=1, currency='EUR'),
                       debited_wallet=legal_user_wallet,
                       bank_account=bankaccount,
                       bank_wire_ref="John Doe's trousers")

payout.save()

```



## KYC (Know Your Customer) / Identification documents

To get identification documents of your customers you need to:

* Create a Document

```python

document = Document(type='IDENTITY_PROOF', user=legal_user)
document.save()

```

* Create a Page with uploaded file encoded in base64

```python

with open(file_path, "rb") as image_file:
    encoded_file = base64.b64encode(image_file.read())

page = Page(document=document, file=encoded_file, user=legal_user)
page.save()

```


To get a list of all the uploaded documents for a particular user:

```python

documents = Document.all(user_id=legal_user.get_pk())

```

To get the list of all the uploaded documents for all users:

```python

documents = Document.all()

```



## Sort and filter lists

To manage your lists you can pass filters and sorting parameters to the method `all`. See this example with a transaction list:

```python

transactions = Transaction.all(handler=handler,
                               user_id=legal_user.get_pk(),
                               status='SUCCEEDED',
                               sort='CreationDate:asc')

```

`status` is a filter and `sort` a sorting parameter.
Please refer to the [documentation](https://docs.mangopay.com/api-references/sort-lists/) to know how to format parameters.
