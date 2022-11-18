from django.db import models


class InvalidFormat(Exception):
    def __init__(self, value):
        super().__init__(f"Identification value has invalid format: {value}.")


class ConstraintError(Exception):
    pass


class Registry(dict):
    def get(self, key, **constraints):
        constraints = frozenset(constraints.items())
        klass, registered_constraints = self[key]

        if not constraints.issubset(registered_constraints):
            raise ConstraintError(f"Key {key} is mapped to {klass} but the constraints {constraints} does not match.")

        return klass

    def filter(self, **constraints):
        constraints = frozenset(constraints.items())

        return {klass for klass, registered_constraints in self.values()
                if constraints.issubset(registered_constraints)}

    def register(self, key, klass, **constraints):
        if key in self:
            raise KeyError(f"Key {key} already exists.")

        self[key] = klass, frozenset(constraints.items())


class Identification(str):
    registry = Registry()

    @property
    def kind(self):
        return type(self).__name__.lower()

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def of_kind(cls, kind, value, **constraints):
        klass = cls.registry.get(kind, **constraints)
        return klass(value)

    @classmethod
    def register(cls, klass, **constraints):
        if not issubclass(klass, cls):
            raise TypeError(f"Class {klass} is not a subtype of {cls}.")

        cls.registry.register(klass.name(), klass, **constraints)

    @classmethod
    def choices(cls):
        return [(key, klass.name) for key, (klass, _) in cls.registry.items()]


class CPFInvalid(InvalidFormat):
    pass


class Cpf(Identification):
    def __new__(cls, string):
        if not cls.checksum(string):
            raise CPFInvalid(string)

        return super().__new__(cls, string)

    def __format__(self, spec):
        if spec == "dot":
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


Identification.register(Cpf, country="BR", person="individual")
Identification.register(Cnpj, country="BR", person="business")


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
