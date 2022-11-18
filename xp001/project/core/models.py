from django.db import models


class IdentException(Exception):
    pass


class IdentAlreadyRegistered(IdentException):
    def __init__(self, klass):
        super().__init__(f"Ident {klass!r} is already registered.")


class IdentNotFound(IdentException):
    def __init__(self, kind):
        super().__init__(f"Ident of kind {kind!r} is not registered.")


class IdentTypeError(IdentException):
    def __init__(self, klass):
        super().__init__(f"Object type {klass!r} not of a subclass of Identification.")


class IdentInvalid(IdentException):
    def __init__(self, value):
        super().__init__(f"Identification value is invalid: {value}.")


class Identification(str):
    kinds = {}

    @property
    def kind(self):
        return type(self).__name__.lower()

    @staticmethod
    def as_key(kind, country=None):
        return kind if country is None else (kind, country)

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def of_kind(cls, kind, value, country=None):
        key = cls.as_key(kind, country)

        if klass := cls.kinds.get(key):
            return klass(value)
        else:
            raise IdentNotFound(kind)

    @classmethod
    def register(cls, klass, country=None):
        if not issubclass(klass, cls):
            raise IdentTypeError(klass)

        if klass in cls.kinds:
            raise IdentAlreadyRegistered(klass)

        cls.kinds[cls.as_key(klass.name(), country)] = klass

    @classmethod
    def choices(cls):
        return list(cls.kinds.items())


class CPFInvalid(IdentInvalid):
    pass


class Cpf(Identification):
    def __new__(cls, string):
        if not cls.checksum(string):
            raise CPFInvalid(string)

        return super().__new__(cls, string)

    def __format__(self, spec):
        if spec == ".":
            return "{0}.{1}.{2}-{3}".format(self[:3], self[3:6], self[6:9], self[9:11])
        else:
            return self

    @staticmethod
    def checksum(value):
        """
        CPF Checksum algorithm.
        """

        def dv(partial):
            s = sum(b * int(v) for b, v in zip(range(len(partial) + 1, 1, -1), partial))
            return s % 11

        dv1 = 11 - dv(value[:9])
        q2 = dv(value[:10])
        dv2 = 11 - q2 if q2 >= 2 else 0

        return dv1 == int(value[9]) and dv2 == int(value[10])


class Cnpj(Identification):
    pass


Identification.register(Cpf)
Identification.register(Cnpj)


class Customer(models.Model):
    identification_value = models.CharField(max_length=256)
    identification_kind = models.CharField(choices=Identification.choices(), max_length=32)

    @property
    def identification(self):
        return Identification.of_kind(self.identification_kind, self.identification_value)

    @identification.setter
    def identification(self, ident):
        if not isinstance(ident, Identification):
            raise IdentTypeError(ident)

        self.identification_kind = ident.kind
        self.identification_value = ident
