from localflavors.registry import Registry


class InvalidFormat(Exception):
    def __init__(self, value):
        super().__init__(f"Identification value has invalid format: {value}.")


class Identification(str):
    pass


class IdentificationFactory:
    registry = Registry()

    @staticmethod
    def key_for(obj):
        klass = type(obj) if isinstance(obj, Identification) else obj
        return klass.__name__.lower()

    @classmethod
    def of_kind(cls, kind, value, **constraints):
        klass = cls.registry.get(kind, **constraints)
        return klass(value)

    @classmethod
    def register(cls, klass, **constraints):
        if not issubclass(klass, Identification):
            raise TypeError(f"Class {klass} is not a subtype of {Identification}.")

        cls.registry.register(cls.key_for(klass), klass, **constraints)

    @classmethod
    def unpack(cls, ident):
        if not isinstance(ident, Identification):
            raise TypeError(f"{ident} is not a subtype of {Identification}.")

        return cls.key_for(ident), ident

    @classmethod
    def choices(cls):
        return [(key, klass.__name__) for key, (klass, _) in cls.registry.items()]
