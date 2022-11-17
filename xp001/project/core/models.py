from django.db import models


class IdentificationTypes(models.TextChoices):
    BRCPF = "BrCpf", "CPF"
    BRCNPJ = "BrCnpj", "CNPJ"
    BRRG = "BrRg", "RG"


class BadCustomer(models.Model):
    identification_value = models.CharField(max_length=256)
    identification_type = models.CharField(choices=IdentificationTypes.choices, max_length=32)


class Identification(str):
    def from_type(type, value):
        if (type == "BrCpf"):
            return Cpf()
        if (type == "BrCnpj"):
            return Cnpj()

class Cpf(Identification):
    pass

class Cnpj(Identification):
    pass

class IdentificationField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = kwargs.get("name")

        self.field_value = models.CharField(max_length=256)
        self.field_type = models.CharField(max_length=32, choices=IdentificationTypes.choices)

    def contribute_to_class(self, cls, name, private_only=True):
        self.field_type_name = f"{name}_type"
        self.field_value_name = f"{name}_value"
        cls.add_to_class(self.field_type_name, self.field_type)
        cls.add_to_class(self.field_value_name, self.field_value)
        super().contribute_to_class(cls, name, private_only)


    def __set__(self, instance, value):
        if not isinstance(value, Identification):
            raise TypeError(f"Expected type Identification, but received {type(value)}.")

        setattr(instance, self.field_value_name, str(value))
        setattr(instance, self.field_type_name, type(value).__name__)


class GoodCustomer(models.Model):
    identification = IdentificationField()
