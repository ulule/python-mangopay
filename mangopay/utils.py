# see: http://hustoknow.blogspot.com/2011/01/m2crypto-and-facebook-python-sdk.html
from __future__ import unicode_literals

import datetime
import decimal
import copy
import inspect
import six
import sys

from functools import wraps
from .exceptions import CurrencyMismatch
from .compat import python_2_unicode_compatible

if six.PY3:
    from urllib import request
    orig = request.URLopener.open_https
    request.URLopener.open_https = orig   # uncomment this line back and forth
elif six.PY2:
    import urllib
    orig = urllib.URLopener.open_https
    urllib.URLopener.open_https = orig


@python_2_unicode_compatible
class Money(object):
    __hash__ = None

    def __init__(self, amount="0", currency=None):
        try:
            self.amount = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            raise ValueError("amount value could not be converted to "
                             "Decimal(): '{}'".format(amount))
        self.currency = currency

    def __repr__(self):
        return "{} {}".format(self.currency, self.amount)

    def __str__(self):
        return force_text("{} {:,.2f}".format(self.currency, self.amount))

    def __lt__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '<')
            other = other.amount
        return self.amount < other

    def __le__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '<=')
            other = other.amount
        return self.amount <= other

    def __eq__(self, other):
        if isinstance(other, Money):
            return ((self.amount == other.amount) and
                    (self.currency == other.currency))
        return False

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '>')
            other = other.amount
        return self.amount > other

    def __ge__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '>=')
            other = other.amount
        return self.amount >= other

    def __bool__(self):
        return bool(self.amount)

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '+')
            other = other.amount
        amount = self.amount + other
        return self.__class__(amount, self.currency)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '-')
            other = other.amount
        amount = self.amount - other
        return self.__class__(amount, self.currency)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError("multiplication is unsupported between "
                            "two money objects")
        amount = self.amount * other
        return self.__class__(amount, self.currency)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '/')

            if other.amount == 0:
                raise ZeroDivisionError()

            return self.amount / other.amount

        if other == 0:
            raise ZeroDivisionError()

        amount = self.amount / other

        return self.__class__(amount, self.currency)

    def __floordiv__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '//')

            if other.amount == 0:
                raise ZeroDivisionError()
            return self.amount // other.amount

        if other == 0:
            raise ZeroDivisionError()

        amount = self.amount // other
        return self.__class__(amount, self.currency)

    def __mod__(self, other):
        if isinstance(other, Money):
            raise TypeError("modulo is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        if other == 0:
            raise ZeroDivisionError()

        amount = self.amount % other
        return self.__class__(amount, self.currency)

    def __divmod__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, 'divmod')

            if other.amount == 0:
                raise ZeroDivisionError()

            return divmod(self.amount, other.amount)

        if other == 0:
            raise ZeroDivisionError()

        whole, remainder = divmod(self.amount, other)

        return (self.__class__(whole, self.currency),
                self.__class__(remainder, self.currency))

    def __pow__(self, other):
        if isinstance(other, Money):
            raise TypeError("power operator is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        amount = self.amount ** other
        return self.__class__(amount, self.currency)

    def __neg__(self):
        return self.__class__(-self.amount, self.currency)

    def __pos__(self):
        return self.__class__(+self.amount, self.currency)

    def __abs__(self):
        return self.__class__(abs(self.amount), self.currency)

    def __int__(self):
        return int(self.amount)

    def __float__(self):
        return float(self.amount)

    def __round__(self, ndigits=0):
        return self.__class__(round(self.amount, ndigits), self.currency)


# This code belongs to https://github.com/carljm/django-model-utils
class Choices(object):
    """
    A class to encapsulate handy functionality for lists of choices
    for a Django model field.
    Each argument to ``Choices`` is a choice, represented as either a
    string, a two-tuple, or a three-tuple.
    If a single string is provided, that string is used as the
    database representation of the choice as well as the
    human-readable presentation.
    If a two-tuple is provided, the first item is used as the database
    representation and the second the human-readable presentation.
    If a triple is provided, the first item is the database
    representation, the second a valid Python identifier that can be
    used as a readable label in code, and the third the human-readable
    presentation. This is most useful when the database representation
    must sacrifice readability for some reason: to achieve a specific
    ordering, to use an integer rather than a character field, etc.
    Regardless of what representation of each choice is originally
    given, when iterated over or indexed into, a ``Choices`` object
    behaves as the standard Django choices list of two-tuples.
    If the triple form is used, the Python identifier names can be
    accessed as attributes on the ``Choices`` object, returning the
    database representation. (If the single or two-tuple forms are
    used and the database representation happens to be a valid Python
    identifier, the database representation itself is available as an
    attribute on the ``Choices`` object, returning itself.)
    Option groups can also be used with ``Choices``; in that case each
    argument is a tuple consisting of the option group name and a list
    of options, where each option in the list is either a string, a
    two-tuple, or a triple as outlined above.
    """

    def __init__(self, *choices):
        # list of choices expanded to triples - can include optgroups
        self._triples = []
        # list of choices as (db, human-readable) - can include optgroups
        self._doubles = []
        # dictionary mapping db representation to human-readable
        self._display_map = {}
        # dictionary mapping Python identifier to db representation
        self._identifier_map = {}
        # set of db representations
        self._db_values = set()

        self._process(choices)

    def _store(self, triple, triple_collector, double_collector):
        self._identifier_map[triple[1]] = triple[0]
        self._display_map[triple[0]] = triple[2]
        self._db_values.add(triple[0])
        triple_collector.append(triple)
        double_collector.append((triple[0], triple[2]))

    def _process(self, choices, triple_collector=None, double_collector=None):
        if triple_collector is None:
            triple_collector = self._triples
        if double_collector is None:
            double_collector = self._doubles

        store = lambda c: self._store(c, triple_collector, double_collector)

        for choice in choices:
            if isinstance(choice, (list, tuple)):
                if len(choice) == 3:
                    store(choice)
                elif len(choice) == 2:
                    if isinstance(choice[1], (list, tuple)):
                        # option group
                        group_name = choice[0]
                        subchoices = choice[1]
                        tc = []
                        triple_collector.append((group_name, tc))
                        dc = []
                        double_collector.append((group_name, dc))
                        self._process(subchoices, tc, dc)
                    else:
                        store((choice[0], choice[0], choice[1]))
                else:
                    raise ValueError(
                        "Choices can't take a list of length %s, only 2 or 3"
                        % len(choice))
            else:
                store((choice, choice, choice))

    def __len__(self):
        return len(self._doubles)

    def __iter__(self):
        return iter(self._doubles)

    def __getattr__(self, attname):
        try:
            return self._identifier_map[attname]
        except KeyError:
            raise AttributeError(attname)

    def __getitem__(self, key):
        return self._display_map[key]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            other = other._triples
        else:
            other = list(other)
        return Choices(*(self._triples + other))

    def __radd__(self, other):
        # radd is never called for matching types, so we don't check here
        other = list(other)
        return Choices(*(other + self._triples))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._triples == other._triples
        return False

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(("%s" % repr(i) for i in self._triples)))

    def __contains__(self, item):
        return item in self._db_values

    def __deepcopy__(self, memo):
        return self.__class__(*copy.deepcopy(self._triples, memo))


def timestamp_from_datetime(dt):
    epoch = datetime.datetime(1970, 1, 1)
    diff = dt - epoch
    return diff.days * 24 * 3600 + diff.seconds


def timestamp_from_date(date):
    epoch = datetime.date(1970, 1, 1)
    diff = date - epoch
    return diff.days * 24 * 3600 + diff.seconds


if six.PY3:
    memoryview = memoryview
else:
    memoryview = buffer  # noqa


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_text(strings_only=True).
    """
    return isinstance(obj, six.integer_types + (type(None), float, decimal.Decimal,
                                                datetime.datetime, datetime.date, datetime.time))


def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first, saves 30-40% when s is an instance of
    # six.text_type. This function gets called often in that setting.
    if isinstance(s, six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, six.string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                if six.PY3:
                    if isinstance(s, bytes):
                        s = six.text_type(s, encoding, errors)
                    else:
                        s = six.text_type(s)
                else:
                    s = six.text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError:
        # If we get to here, the caller has passed in an Exception
        # subclass populated with non-ASCII bytestring data without a
        # working unicode method. Try to handle this without raising a
        # further exception by individually forcing the exception args
        # to unicode.
        s = ' '.join([force_text(arg, encoding, strings_only,
                                 errors) for arg in s])
    return s


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, memoryview):
        s = bytes(s)
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join([force_bytes(arg, encoding, strings_only,
                                              errors) for arg in s])
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)


if six.PY3:
    force_str = force_text
else:
    force_str = force_bytes


def memoize(func, cache, num_args):
    """
    Wrap a function so that results for any argument tuple are stored in
    'cache'. Note that the args to the function must be usable as dictionary
    keys.
    Only the first num_args are considered when creating the key.
    """
    @wraps(func)
    def wrapper(*args):
        mem_args = args[:num_args]
        if mem_args in cache:
            return cache[mem_args]
        result = func(*args)
        cache[mem_args] = result
        return result
    return wrapper


def reraise_as(new_exception_or_type):
    """
    Obtained from https://github.com/dcramer/reraise/blob/master/src/reraise.py
    >>> try:
    >>>     do_something_crazy()
    >>> except Exception:
    >>>     reraise_as(UnhandledException)
    """
    __traceback_hide__ = True  # NOQA

    e_type, e_value, e_traceback = sys.exc_info()

    if inspect.isclass(new_exception_or_type):
        new_type = new_exception_or_type
        new_exception = new_exception_or_type()
    else:
        new_type = type(new_exception_or_type)
        new_exception = new_exception_or_type

    new_exception.__cause__ = e_value

    try:
        six.reraise(new_type, new_exception, e_traceback)
    finally:
        del e_traceback
