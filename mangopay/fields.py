import re
import time
import datetime
import six

from .utils import (Address, timestamp_from_datetime, timestamp_from_date,
                    Money, Reason, Birthplace)
import sys


class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.att_name = self.field.name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance._data.get(self.att_name)

        return self.field

    def __set__(self, instance, value):
        instance._data[self.att_name] = value


class Field(object):
    default = None
    _field_counter = 0
    _order = 0

    def get_attributes(self):
        return {}

    def __init__(self, null=False, api_name=None,
                 help_text=None, api_value_callback=None,
                 choices=None, default=None,
                 python_value_callback=None, *args, **kwargs):
        self.null = null
        self.attributes = self.get_attributes()
        self.default = kwargs.get('default', None)
        self.api_name = api_name
        self.api_value_callback = api_value_callback
        self.python_value_callback = python_value_callback
        self.help_text = help_text
        self.required = kwargs.get('required', False)
        self.choices = choices
        self.default = default

        self.attributes.update(kwargs)

        self._order = Field._field_counter

    def add_to_class(self, klass, name):
        self.name = name
        self.model = klass
        self.api_name = self.api_name or re.sub('_+', ' ', name).title()

        klass._meta.fields[self.name] = self

        setattr(klass, name, FieldDescriptor(self))

    def null_wrapper(self, value, default=None):
        if (self.null and not value) or not default:
            return value
        return value or default

    def api_value(self, value):
        if self.api_value_callback:
            value = self.api_value_callback(value)
        return value

    def python_value(self, value):
        if self.python_value_callback:
            value = self.python_value_callback(value)
        return value


class CharField(Field):
    def python_value(self, value):
        if self.python_value_callback:
            value = self.python_value_callback(value)

        if isinstance(value, six.string_types):
            if sys.version_info < (3, 0) and isinstance(value, unicode):
                return value.encode('utf-8')

        return value

    def api_value(self, value):
        if sys.version_info > (3, 0) and isinstance(value, six.binary_type):
            return value.decode('utf-8')

        return value


class DateTimeField(Field):
    def python_value(self, value):
        value = super(DateTimeField, self).python_value(value)

        if isinstance(value, six.string_types):
            value = value.rsplit('.', 1)[0]
            value = datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6])

        if isinstance(value, six.integer_types):
            value = datetime.datetime.utcfromtimestamp(value)

        return value

    def api_value(self, value):
        value = super(DateTimeField, self).api_value(value)

        if isinstance(value, datetime.datetime):
            value = timestamp_from_datetime(value)

        return value


class DateField(Field):
    def python_value(self, value):
        value = super(DateField, self).python_value(value)

        if isinstance(value, six.string_types):
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()

        if isinstance(value, six.integer_types):
            value = datetime.date.fromtimestamp(value)

        return value

    def api_value(self, value):
        value = super(DateField, self).api_value(value)

        if isinstance(value, datetime.date):
            value = timestamp_from_date(value)

        return value


class IntegerField(Field):
    def api_value(self, value):
        return self.null_wrapper(super(IntegerField, self).api_value(value), 0)

    def python_value(self, value):
        if value is not None:
            return int(super(IntegerField, self).python_value(value))


class FloatField(Field):
    def api_value(self, value):
        return self.null_wrapper(super(FloatField, self).api_value(value), 0.0)

    def python_value(self, value):
        if value is not None:
            return float(super(FloatField, self).python_value(value))


class PrimaryKeyField(IntegerField):
    pass


class ListField(Field):
    pass


class BooleanField(IntegerField):
    def api_value(self, value):
        value = super(BooleanField, self).api_value(value)

        if value:
            return 1
        return 0

    def python_value(self, value):
        value = super(BooleanField, self).python_value(value)

        return bool(value)


class EmailField(CharField):
    pass


class MoneyField(Field):
    def python_value(self, value):
        if value is not None:
            return Money(currency=value['Currency'], amount=value['Amount'])

        return value

    def api_value(self, value):
        value = super(MoneyField, self).api_value(value)

        if isinstance(value, Money):
            value = {
                'Currency': value.currency,
                'Amount': int(value.amount)
            }

        return value


class DisputeReasonField(Field):
    def python_value(self, value):
        if value is not None:
            return Reason(type=value['DisputeReasonType'], message=value['DisputeReasonMessage'])

        return value

    def api_value(self, value):
        value = super(DisputeReasonField, self).api_value(value)

        if isinstance(value, Reason):
            value = {
                'DisputeReasonType': value.type,
                'DisputeReasonMessage': str(value.message)
            }

        return value


class ReverseOneToOneRelatedObject(object):
    def __init__(self, related_model, name):
        self.field_name = name
        self.related_model = related_model

    def __get__(self, instance, instance_type=None):
        return instance.one(self.related_model)


class ForeignKeyField(IntegerField):
    def __init__(self, to, related_name=None, *args, **kwargs):
        self.to = to
        self.related_name = related_name

        super(ForeignKeyField, self).__init__(*args, **kwargs)

    def add_to_class(self, klass, name):
        self.descriptor = name
        self.name = name + '_id'
        self.model = klass

        self.api_name = self.api_name or re.sub('_', ' ', name).title()

        if self.related_name is None:
            self.related_name = klass._meta.verbose_name + '_set'

        klass._meta.rel_fields[name] = self.name
        setattr(klass, self.descriptor, ForeignRelatedObject(self.to, self.name))
        setattr(klass, self.name, None)

        reverse_rel = ReverseForeignRelatedObject(klass, self.name)
        setattr(self.to, self.related_name, reverse_rel)
        self.to._meta.reverse_relations[self.related_name] = klass

    def api_value(self, value):
        from .base import BaseApiModel
        value = super(ForeignKeyField, self).api_value(value)

        if isinstance(value, BaseApiModel):
            value = value.get_pk()

        return value


class OneToOneField(ForeignKeyField):
    def add_to_class(self, klass, name):
        self.descriptor = name
        self.name = name + '_id'
        self.model = klass

        self.api_name = self.api_name or re.sub('_', ' ', name).title()

        if self.related_name is None:
            self.related_name = klass._meta.verbose_name

        klass._meta.rel_fields[name] = self.name
        setattr(klass, self.descriptor, ForeignRelatedObject(self.to, self.name))
        setattr(klass, self.name, None)

        reverse_rel = ReverseOneToOneRelatedObject(klass, self.name)
        setattr(self.to, self.related_name, reverse_rel)
        self.to._meta.reverse_relations[self.related_name] = klass


class ForeignRelatedObject(object):
    def __init__(self, to, name):
        self.field_name = name
        self.to = to
        self.cache_name = '_cache_%s' % name

    def __get__(self, instance, instance_type=None):
        if not getattr(instance, self.cache_name, None):
            id = getattr(instance, self.field_name, 0)
            related = self.to.select().get(id, handler=instance.handler)
            setattr(instance, self.cache_name, related)
        return getattr(instance, self.cache_name)

    def __set__(self, instance, obj):
        assert isinstance(obj, self.to), "Cannot assign %s, invalid type" % obj
        setattr(instance, self.field_name, obj.get_pk())
        setattr(instance, self.cache_name, obj)


class ReverseForeignRelatedObject(object):
    def __init__(self, related_model, name):
        self.field_name = name
        self.related_model = related_model

    def __get__(self, instance, instance_type=None):
        return RelatedManager(instance, self.related_model)


class RelatedManager(object):
    def __init__(self, instance, related_model):
        self.instance = instance
        self.related_model = related_model

    def get(self, pk, **kwargs):
        return self.instance.get(pk, self.instance.handler, self.related_model, **kwargs)

    def all(self):
        return self.instance.list(self.related_model)


class ManyToManyField(ListField):
    def __init__(self, to, related_name=None, *args, **kwargs):
        self.to = to
        self.related_name = related_name

        super(ManyToManyField, self).__init__(*args, **kwargs)

    def add_to_class(self, klass, name):
        self.descriptor = name
        self.name = name + '_ids'
        self.model = klass

        self.api_name = self.api_name or re.sub('_', ' ', name).title()

        if self.related_name is None:
            self.related_name = klass._meta.verbose_name + '_set'

        klass._meta.rel_fields[name] = self.name
        setattr(klass, self.descriptor, ManyToManyRelatedObject(self.to, self.name))
        setattr(klass, self.name, None)

        reverse_rel = ManyToManyRelatedObject(klass, self.name)

        setattr(self.to, self.related_name, reverse_rel)
        self.to._meta.reverse_relations[self.related_name] = klass

    def api_value(self, value):
        from .base import BaseApiModel

        values = super(ManyToManyField, self).api_value(value)

        for i in range(len(values)):
            if isinstance(value, BaseApiModel):
                value = value.get_pk()
                values[i] = value

        return values


class ManyToManyRelatedObject(object):
    def __init__(self, related_model, name):
        self.related_model = related_model
        self.field_name = name

    def __get__(self, instance, instance_type=None):
        return instance.list(self.related_model)

    def __set__(self, instance, objs):
        setattr(instance, self.field_name, [obj.get_pk() for obj in objs])


class BirthplaceField(Field):
    def python_value(self, value):
        if value is not None:
            return Birthplace(city=value['City'], country=value['Country'])

        return value

    def api_value(self, value):
        value = super(BirthplaceField, self).api_value(value)

        if isinstance(value, Birthplace):
            value = {
                'City': value.city,
                'Country': value.country,
            }

        return value


class AddressField(Field):
    def python_value(self, value):
        if value is not None:
            return Address(address_line_1=value['AddressLine1'], address_line_2=value['AddressLine2'],
                           city=value['City'], region=value['Region'],
                           postal_code=value['PostalCode'], country=value['Country'])

        return value

    def api_value(self, value):
        value = super(AddressField, self).api_value(value)

        if isinstance(value, Address):
            value = {
                'AddressLine1': value.address_line_1,
                'AddressLine2': value.address_line_2,
                'City': value.city,
                'Region': value.region,
                'PostalCode': value.postal_code,
                'Country': value.country
            }

        return value
